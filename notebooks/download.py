import gdelt
import os
from tqdm import tnrange
import sys
import warnings
import pandas as pd
import requests
import urllib3
import time

if __name__ == "__main__":
    year = "2019"
    month = "06"
    day = "05"
    gd2 = gdelt.gdelt(version=2)
    results = gd2.Search(['{} {} {}'.format(year, month, day)],
                         table='events',coverage=True)
    print(results.shape)