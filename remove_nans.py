import os
import argparse
from shutil import copyfile
import numpy as np
import pandas as pd
from tqdm import tqdm


def copy_files(filepaths):
    for filepath in filepaths:
        copyfile(filepath, filepath + '.backup')


def get_non_nans_columns(df):
    result = []
    item0 = df.iloc[0]
    columns = df.columns
    for column in columns:
        if not column.startswith('smart_'):
            result.append(column)
        elif not np.isnan(item0[column]):
            result.append(column)
    return result


def remove_nans_from_file(filepath):
    df = pd.read_csv(filepath)
    columns = get_non_nans_columns(df)
    df = df[columns]
    df.to_csv(filepath, index=False)


def remove_nans_from_files(filepaths):
    for filepath in tqdm(filepaths):
        remove_nans_from_file(filepath)


def remove_nans(filepaths, replace):
    if not replace: # make backup
        copy_files(filepaths)
        print('Files were copied')
    remove_nans_from_files(filepaths)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process arguments')
    parser.add_argument('-csv', '--csv', type=str, action='append')
    parser.add_argument('-replace', '--replace', action='store_true')
    return parser.parse_args()


def check_args(args):
    for filepath in args.csv:
        if not os.path.exists(filepath):
            raise RuntimeError("Filepath {} doesn't exist".format(filepath))


if __name__ == '__main__':
    args = parse_arguments()
    check_args(args)
    remove_nans(args.csv, args.replace)

