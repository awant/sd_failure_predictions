import os
import argparse
from tqdm import tqdm
from collections import defaultdict, namedtuple
import pandas as pd


YearPath = namedtuple('YearPath', ['year', 'path'])


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


class SerialNumber(object):
    def __init__(self, serial_number, first_seen):
        self.serial_number = serial_number
        self.last_seen = self.first_seen = first_seen
        self.failure = False
        self.failure_date = None

    def set_failure(self, failure_date):
        self.failure = True
        self.failure_date = failure_date

    def update(self, date):
        self.last_seen = date


class ModelBucket(object):
    def __init__(self):
        self.model = None
        self.serial_numbers = {}
        self._failured_serial_number = 0

    def add(self, serial_number, date, failure):
        if serial_number not in self.serial_numbers:
            self.serial_numbers[serial_number] = SerialNumber(serial_number, date)
            return
        self.serial_numbers[serial_number].update(date)
        if failure:
            self.serial_numbers[serial_number].set_failure(date)
            self._failured_serial_number += 1

    @property
    def n_serial_numbers(self):
        return len(self.serial_numbers)

    @property
    def n_failures(self):
        return self._failured_serial_number



class SDStats(object):
    def __init__(self):
        self.model_buckets = defaultdict(ModelBucket)

    @property
    def n_models(self):
        return len(self.model_buckets)

    def add(self, sample):
        model, sn = sample['model'], sample['serial_number']
        date, failure = sample['date'], sample['failure']
        self.model_buckets[model].add(sn, date, failure)
        self.model_buckets[model].model = model

    def most_unreliable(self, n=5):
        sorted_model_buckets = list(map(lambda x: (x.n_failures, x), self.model_buckets.values()))
        sorted_model_buckets = sorted(sorted_model_buckets, key=lambda x: x[0], reverse=True)
        return list(zip(*sorted_model_buckets[:5]))[1]


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


def iget_next_csv(folder):
    years_directories = get_dirs_with_years(folder)  # sorted by year
    for year_path in years_directories:
        yield from sorted(list(iget_next_file(year_path.path, '.csv')))


def icollect_stats(folder, years=None):
    # year, model, serial_number, first_time_seen, last_time_seen, failure, failure_date
    current_year, stats_by_year = None, SDStats()
    for csv_filename, csv_filepath in tqdm(iget_next_csv(folder)):
        year = int(csv_filename[:4])
        if years and (year not in years):
            continue
        current_year = current_year if current_year else year
        df = pd.read_csv(csv_filepath)
        if year != current_year:  # csv's sorted by year
            yield current_year, stats_by_year
            current_year, stats_by_year = year, SDStats()
        for index, sample in df.iterrows():
            stats_by_year.add(sample)
        del df
    if current_year:  # at least one record
        yield current_year, stats_by_year


def show_stats(stats, year):
    print('\n--- {} ---, unique models: {}'.format(year, stats.n_models))
    for model_bucket in stats.most_unreliable(5):  # show 5 most unreliable models
        print('  model: {:30}\tserial_numbers: {:8}\tfailures: {:10}'\
                .format(model_bucket.model, model_bucket.n_serial_numbers, model_bucket.n_failures))


def save_stats(stats, filepath, year):
    ext_idx = filepath.rfind('.')
    ext_idx = len(filepath) if ext_idx == -1 else ext_idx
    out_fp = ''.join([filepath[:ext_idx], '_', str(year), filepath[ext_idx:]])
    rows = []
    for model, model_bucket in stats.model_buckets.items():
        for serial_number, sn_obj in model_bucket.serial_numbers.items():
            rows.append({
                'year': year,
                'model': model,
                'serial_number': serial_number,
                'first_time_seen': sn_obj.first_seen,
                'last_time_seen': sn_obj.last_seen,
                'failure': sn_obj.failure,
                'failure_date': sn_obj.failure_date
            })
    df = pd.DataFrame(rows)
    df.to_csv(out_fp, index=False)
    print('saved stats to {}'.format(out_fp))
    return out_fp


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process arguments')
    parser.add_argument('--dump', action='store_true')
    parser.add_argument('--stats_filepath', type=str, default=os.path.join('data', 'stats.csv'))
    parser.add_argument('--folder', type=str, default='data')
    parser.add_argument('-y', '--year', type=int, action='append')
    return parser.parse_args()


def check_args(args):
    if not os.path.exists(args.folder):
        raise RuntimeError("Folder {} doesn't exist".format(arg.folder))


if __name__ == '__main__':
    args = parse_arguments()
    check_args(args)
    for year, stats in icollect_stats(args.folder, args.year):
        show_stats(stats, year)
        if args.dump:
            save_stats(stats, args.stats_filepath, year)

