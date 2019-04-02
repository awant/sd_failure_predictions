import os
import argparse
import requests
from tqdm import tqdm
import zipfile


class BackBlaze(object):
    # https://www.backblaze.com/b2/hard-drive-test-data.html
    LINK_TEMPLATE = 'https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_{time}.zip'
    DATASET_TIMES = {
            2013: [],
            2014: [],
            2015: [],
            2016: [1, 2, 3, 4],
            2017: [1, 2, 3, 4],
            2018: [1, 2, 3, 4]
    }

    def __init__(self, folder, years=[], with_stats=False):
        self.folder = folder
        self.years = years
        self._compute_stats = with_stats
        self._check_years()
        self._prepare_folder()

    def _prepare_folder(self):
        if os.path.exists(self.folder):
            print("Warning: Folder {} exists".format(self.folder))
        os.makedirs(self.folder)

    def _check_years(self):
        for year in self.years:
            if year not in self.DATASET_TIMES:
                raise RuntimeError("Year {} not exists".format(year))

    def _form_url(self, year, q=None):
        time = str(year)
        if q is not None:
            time = 'Q{}_'.format(q) + time
        return self.LINK_TEMPLATE.format(time=time)

    def _form_zipfilepath(self, year, q):
        time_line = str(year)
        time_line += '_{}'.format(q) if q else ''
        return os.path.join(self.folder, 'data_{}.zip'.format(time_line))

    def _download_file(self, url, filepath):
        response = requests.get(url, stream=True)
        with open(filepath, 'wb') as f:
            for data in tqdm(response.iter_content(chunk_size=256*1024*1024)):
                f.write(data)

    def _unzip_file(self, filepath):
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(path=self.folder)

    def _get_times(self):
        times = []
        for year in self.years:
            qs = self.DATASET_TIMES[year]
            qs = qs if qs else [None]
            times += [(year, q) for q in qs]
        return times

    def _compute_statistics(self):
        raise RuntimeError("TODO:")

    def load(self):
        times = self._get_times()
        for year, q in tqdm(times, total=len(times), desc='Downloading files'):
            url = self._form_url(year, q)
            zipfilepath = self._form_zipfilepath(year, q)
            self._download_file(url, zipfilepath)
            self._unzip_file(zipfilepath)
            os.remove(zipfilepath)
        if self._compute_stats:
            self._compute_statistics()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process arguments')
    parser.add_argument('--backblaze', action='store_true')
    parser.add_argument('--tgt_folder', type=str, default='data')
    parser.add_argument('-y', '--year', nargs='+', type=int, required=True)
    parser.add_argument('--with_stats', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    if args.backblaze:
        storage = BackBlaze(args.tgt_folder, years=args.year, with_stats=args.with_stats)
    else:
        raise RuntimeError("A storage is unknown")
    storage.load()

