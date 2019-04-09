
### Data understanding

5 most unreliable models (models with most failures count):

--- 2015 ---, unique models: 78
| model                   | serial_numbers | failures |
|-------------------------|----------------|----------|
| ST4000DM000             | 29670          | 585      |
| Hitachi HDS722020ALA330 | 4683           | 108      |
| ST31500541AS            | 1693           | 107      |
| ST3000DM001             | 1168           | 106      |
| WDC WD30EFRX            | 1209           | 78       |

--- 2016 ---, unique models: 77
| model                   | serial_numbers | failures |
|-------------------------|----------------|----------|
| ST4000DM000             | 35678          | 931      |
| ST320LT007              | 73             | 63       |
| ST8000DM002             | 8715           | 46       |
| Hitachi HDS722020ALA330 | 4503           | 43       |
| Hitachi HDS5C3030ALA630 | 4563           | 36       |

--- 2017 ---, unique models: 68
| model                | serial_numbers | failures |
|----------------------|----------------|----------|
| ST4000DM000          | 35189          | 1062     |
| ST8000DM002          | 9979           | 91       |
| ST8000NM0055         | 14509          | 88       |
| HGST HMS5C4040BLE640 | 16251          | 86       |
| ST4000DX000          | 185            | 44       |

--- 2018 ---, unique models: 61
| model                | serial_numbers | failures |
|----------------------|----------------|----------|
| ST4000DM000          | 32164          | 579      |
| ST12000NM0007        | 32638          | 292      |
| ST8000NM0055         | 14508          | 125      |
| ST8000DM002          | 9965           | 91       |
| HGST HMS5C4040BLE640 | 15382          | 54       |

Also, several hard drives are marked as failured, but they are still in logs after that date.

Lets take 2017 year for instance:

| model          | serial_numbers       | first_time_seen | last_time_seen | failure_date |
|----------------|----------------------|-----------------|----------------|--------------|
| ST4000DM000    | Z300XGNY             | 2017-01-01      | 2017-08-27     | 2017-08-26   |
| ST4000DM000    | Z305FSJK             | 2017-01-01      | 2017-12-31     | 2017-02-14   |
| ST4000DX000    | Z1Z04SMV             | 2017-01-01      | 2017-02-21     | 2017-02-20   |
| ST4000DM000    | Z304L92J             | 2017-01-01      | 2017-12-31     | 2017-02-04   |
| PL1331LAHD1K7H | HGST HMS5C4040BLE640 | 2017-02-14      | 2017-07-22     | 2017-02-15   |

We can check these disks by 9 S.M.A.R.T. attribute (Power-On Hours).
Most likely they were taken for tests after marked as failured and then were returned into DC.

