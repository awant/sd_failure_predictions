
## Hard drive failure prediction based on S.M.A.R.T. attributes

Dataset url: https://www.kaggle.com/awant08/hard-drive-failure-prediction-st4000dm000#model_2018_ST4000DM000.csv

### Main goal of the research

The purpose of this repository is:

1. To reproduce results from articles on the same dataset

2. To compare results. Create pivot tables

3. To create the most accurate model

# Articles

1. [Predictive models of hard drive failures based on operational data](https://hal.archives-ouvertes.fr/hal-01703140/document), 2018

2. [Hard Drive Failure Prediction Using Classification and Regression Trees](https://www.researchgate.net/publication/286602543_Hard_Drive_Failure_Prediction_Using_Classification_and_Regression_Trees), 2014

3. [Random-forest-based failure prediction for hard disk drives](https://journals.sagepub.com/doi/full/10.1177/1550147718806480), 2018

4. [Proactive Prediction of Hard Disk Drive Failure](http://cs229.stanford.edu/proj2017/final-reports/5242080.pdf), 2017

5. [Hard Drive Failure Prediction for Large Scale Storage System](https://escholarship.org/uc/item/11x380ng), 2017

6. [Improving Storage System Reliability with Proactive Error Prediction](https://www.usenix.org/system/files/conference/atc17/atc17-mahdisoltani.pdf), 2017

7. [Predicting Disk Replacement towards Reliable Data Centers](https://www.kdd.org/kdd2016/papers/files/adf0849-botezatuA.pdf)

8. [Machine Learning Methods for Predicting Failures in Hard Drives: A Multiple-Instance Application](http://jmlr.csail.mit.edu/papers/volume6/murray05a/murray05a.pdf), 2005

9. [Anomaly detection using SMART indicators for hard disk drive failure prediction](https://www.etran.rs/common/pages/proceedings/IcETRAN2017/RTI/IcETRAN2017_paper_RTI1_6.pdf), 2017

10. [Failure Trends in a Large Disk Drive Population](https://static.googleusercontent.com/media/research.google.com/en//archive/disk_failures.pdf), 2007

11. [Improving Service Availability of Cloud Systems by Predicting Disk Error](https://www.usenix.org/system/files/conference/atc18/atc18-xu-yong.pdf), 2018

12. [Proactive error prediction to improve storage system reliability](https://www.usenix.org/system/files/conference/atc17/atc17-mahdisoltani.pdf), 2017

13. [A PROACTIVE DRIVE RELIABILITY MODEL TO PREDICT FAILURES IN THE HARD DISK DRIVES](http://www.iraj.in/journal/journal_file/journal_pdf/3-78-140957031862-68.pdf), 2014

### Dataset

At the time of the research there was data from BackBlaze up to 2018 year.
Lets take data from 2015 to 2018 year. Test data is data from 4th quarter of 2018 year.

### Metrics

Main metrics are FAR and FDR. These metrics are very popular in hard drive prediction applications.

### Articles analysis

7. Predicting Disk Replacement towards Reliable Data Centers


# Scripts

## download_dataset.py

Download dataset from external storages (BackBlaze only by now)

Download selected years:

```console
python download_dataset.py --backblaze -y 2015 -y 2016 -y 2017 -y 2018
```

## collect_stats.py

Collect stats (some key information) about every hd (serial number) like: 1) working days, 2) failure or not, etc.

Downloaded dataset should be specified. An example:

```console
python collect_stats.py --dump --stats_filepath stats.csv --folder /data
```

## collect_data.py

Collect data from dataset according to stats about specific model. After that there will be a .csv file with processed data.

This script is used to choose data for training. Dump only specific dates before hd failure. (ST4000DM000 by default)

```console
python collect_data.py --model ST4000DM000 --path data/2018/ --stats stats_2018.csv
```

## remove_nans.py

After collecting a data you can remove NANs.
'--replace' flag removes an original file.

```console
python remove_nans.py -csv model_2015_ST4000DM000.csv --replace
```

All in all, you can run these scripts together:

```console
python download_dataset.py --backblaze -y 2015 -y 2016 -y 2017 -y 2018
python collect_stats.py --dump --stats_filepath stats.csv --folder data

python collect_data.py --path data/2015 --stats stats_2015.csv
python collect_data.py --path data/2016 --stats stats_2016.csv
python collect_data.py --path data/2017 --stats stats_2017.csv
python collect_data.py --path data/2018 --stats stats_2018.csv

python remove_nans.py -csv model_2015_ST4000DM000.csv \
                      -csv model_2016_ST4000DM000.csv \
                      -csv model_2017_ST4000DM000.csv \
                      -csv model_2018_ST4000DM000.csv
```


# Results

Setting:
1. ST4000DM000
2. TRAIN DATASET: from 2015 to 2017
3. TEST DATASET: 2018 (6130 health, 218 failured)

| model         | FAR   | FDR   |
|---------------|-------|-------|
| KDD hardcoded | 0.041 | 0.463 |
| RNN  Net      | 0.006 | 0.266 |
| Dense Net 32  | 0.012 | 0.312 |
| Dense Net 8   | 0.004 | 0.252 |
| Dense Net 8,8 | 0.985 | 0.972 |

