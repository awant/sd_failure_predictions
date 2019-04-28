import os
import argparse
from tqdm import tqdm
import pandas as pd
import random
from datetime import datetime, timedelta
import csv


# Lets take data according to these rules:
# Healthy serial drives: N days from random start date for M serial drives
# Failured serial drives: N days before failure (failures - all)
# By default N = 120, M = 10k

random.seed(17)


def get_dirs_with_years(folder):
    MIN_YEAR, MAX_YEAR = 2010, 3000
    directories = os.listdir(folder)
    filtered_dirs = []
    for d in directories:
        year = d[-4:]
        if not year.isdigit():
            continue
        year = int(year)
        if not (MIN_YEAR < year < MAX_YEAR):
            continue
        filtered_dirs.append(YearPath(year, os.path.join(folder, d)))
    filtered_dirs.sort()
    return filtered_dirs


def iget_next_file(folder, ext=None):
    if ext is not None:
        if ext[0] != '.':
            raise RuntimeError("extention should start with '.'")
    for dirpath, dnames, fnames in os.walk(folder):
        for filename in fnames:
            if filename[0] in ['_', '.']:
                continue
            if ext is not None and filename[-len(ext):] != ext:
                continue
            yield filename, os.path.join(dirpath, filename)


def iget_next_csv(folder):
    years_directories = get_dirs_with_years(folder)  # sorted by year
    for year_path in years_directories:
        yield from sorted(list(iget_next_file(year_path.path, '.csv')))


def convert_str2date(line):
    return datetime.strptime(line, "%Y-%m-%d")


def convert_date2str(d):
    return d.strftime("%Y-%m-%d")


def get_available_serial_numbers(stats_path, model, history, health_drives_count):
    def add_days(date: str, days: int):
        date = convert_str2date(date)
        return convert_date2str(date + timedelta(days=days))

    df = pd.read_csv(stats_path)
    df = df[(df.model == model) & (~df.failure | (df.failure_date == df.last_time_seen))]
    df['lifetime_days'] = (df.last_time_seen.apply(convert_str2date) - df.first_time_seen(convert_str2date)).days + 1
    df = df[df.lifetime_days >= history]
    # all failured drives
    df_failured = df[df.failure]
    df_healthy = df[~df.failure]
    # form failured serial numbers
    df_failured_serial_numbers = {
        sn: (start_date, add_days(start_date, history))  # [) interval
        for sn, start_date in df_failured[['serial_number', 'first_time_seen']].values
    }
    df_failured_serial_numbers_count = len(df_failured_serial_numbers)
    # form healthy serial numbers
    if health_drives_count < df_healthy.shape[0]:
        df_healthy = df_healthy.sample(health_drives_count)

    def choose_start_date(obj):
        first_date, lifetime_days = convert_str2date(obj['first_time_seen']), obj['lifetime_days']
        shift_in_days = random.randint(0, lifetime_days - history - 1)
        return convert_date2str(first_date + timedelta(days=shift_in_days))

    def form_interval(row):
        start_date = choose_start_date(row)
        end_date = add_days(start_date, history)
        return start_date, end_date

    df_healthy_serial_numbers = {
            row['serial_number']: form_interval(row) for _, row in df_healthy.iterrows()
    }
    return df_failured_serial_numbers, df_healthy_serial_numbers


def set_out_path(model):
    return 'model_{}.csv'.format(model)


def dump_data(in_path, out_path, failured_sns, healthy_sns):
    sns = {**failured_sns, **healthy_sns}

    def valid_row(row):
        serial_number = row['serial_number']
        if serial_number not in sns:
            return False
        start, end = sns[serial_number]
        return start <= row['date'] < end

    header = None
    with open(out_path, 'w') as out_csv:
        csv_writer = None
        for _, csv_filepath in tqdm(iget_next_csv(in_path)):
            with open(csv_filepath) as inp_csv:
                csv_reader = csv.DictReader(inp_csv)
                for row in reader:
                    if csv_writer:
                        if not valid_row(row):
                            continue
                        csv_writer.writerow(row)
                        continue
                    header = row.keys()
                    csv_writer = csv.DictWriter(out_csv, fieldnames=header)
                    csv_writer.writeheader()
    print('Dump data into: {}'.format(out_path))


def collect_data(in_path, stats_path, out_path, model, history, health_drives_count):
    if not os.path.isdir(in_path):
        RuntimeError('Input filepath should be folder, got: {}'.format(in_path))
    out_path = set_out_path(model) if out_path is None else out_path
    failured_sns, healthy_sns = get_available_serial_numbers(stats_path, model, history, health_drives_count)
    dump_data(in_path, out_path, failured_sns, healthy_sns)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process arguments')
    parser.add_argument('--path', type=str, required=True)
    parser.add_argument('--stats', type=str, required=True)
    parser.add_argument('--out', type=str, default=None)

    parser.add_argument('--model', type=str, default='ST4000DM000')
    parser.add_argument('--days_before', type=int, default=120)
    parser.add_argument('--health_drives', type=int, default=10*1000)
    return parser.parse_args()


def check_args(args):
    pass


if __name__ == '__main__':
    args = parse_arguments()
    check_args(args)
    collect_data(args.path, args.stats, args.out,
        args.model, args.days_before, args.health_drives)

