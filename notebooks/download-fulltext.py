from newsplease import NewsPlease
import pandas as pd
import nltk
from tqdm import tnrange
import re
import multiprocessing
import pickle
import os
import tensorflow as tf
from typing import List, Any
import argparse

relevant_words = ['land', 'forest', 'agriculture', 
                  'farm', 'farmer', 'plantation', 'agrarian',
                  'smallholder', 'grazing', 'development', 'habitat', 
                  'resource', 'cattle', 'dispute', 'strife', 'peat',
                  'rice', 'palm oil', 'sugarcane', 'cassava', 'coconut',
                  'corn', 'mango', 'orange', 'maize', 'wheat', 'sorghum',
                  'bananas', 'tomatoes', 'citrus',
                  'livestock', 'kill', 'dead', 'airport',
                  'aluminum', 'mining', 'agro', 'dam',
                  'road', 'infrastructure', 'transmission', 
                  'conservation', 'settlement', 'displace',
                  'exile', 'caste', 'conflict', 'relocation',
                  'village', 'encroach', 'fertilizer', 'mine',
                  'illegal mining', 'malnutrition', 'contamination',
                  'mangrove', 'water', 'cow', 'cattle', 'appropriation', 
                  'appropriated', 'protest', 'environmental', 'pollution',
                  'copper', 'iron', 'timber', 'acre', 'hectare', ]

days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def load_month(country: str,
             year: int,
             month: int) -> pd.DataFrame:
    
    '''
    Loads the data downloaded in 1-download-gdelt for each day in input
    month and year for input country, returns a list of dataframes.
    
    Parameters
     country (str): either of 'brazil', 'indonesia', 'mexico'
     year (int): either of [2017, 2018, 2019]
     month (int): calendar month as integer
     
    Returns
     dfs (list): list of pandas DataFrames
    '''
    
    dfs = []
    for day in range(days_per_month[month - 1] + 1): 
        file = (input_folder + str(year) + str(month).zfill(2) 
                + str(day).zfill(2) + ".csv")
        if os.path.exists(file):
            file = pd.read_csv(file)
            dfs.append(file)
    return dfs

def find_link_to_scrape(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Identifies unique links to scrape for a single dataframe
    '''
    
    df['to_scrape'] = ''
    df['title'] = ''
    for i in range(len(df)):
        links = df['SOURCEURL'][i]
        l = re.findall(r'\w+(?:-\w+)+', links)
        if l:
            title = max(l, key = len)
            title = title.replace('-', ' ')
            df['title'][i] = title
            if any(word in title for word in relevant_words):
                df['to_scrape'][i] = str(links)
    return df

def combine_days(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    '''
    Combines a list of dataframes and returns a reset index
    '''
    df_parsed = [find_link_to_scrape(dfs[x]) for x in tnrange(len(dfs))]
    df_month = pd.concat(df_parsed)
    df_subs = df_month[df_month['to_scrape'] != '']
    df_subs = df_subs.reset_index()
    return df_subs

def save_obj(obj: Any, name: str, folder: str) -> None:
    'Helper function using pickle to save and load objects'
    with open(folder + name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
def download_url(url: str) -> None:
    try:
        article = NewsPlease.from_url(urls[url], timeout=10)
        save_obj(article, str(url).zfill(5), text_output_folder)
        return 1
    except Exception as ex:
        print(url, ex)
        return 0

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--month", help = "Calendar month to scrape", required=True)
  args = parser.parse_args()


  year = str(2017)
  month = str(args.month).zfill(2)
  country = "brazil"
  text_output_folder = "../data/{}/text/{}/{}/".format(country, str(year), str(month).zfill(2))

  print("Loading {} - {}/{}".format(country, month, year))
  df = pd.read_csv("../data/{}/metadata/{}/{}.csv".format(country, year, month.zfill(2)))
  urls = df['to_scrape'].unique()

  mapping_dictionary = {}
  for i, val in enumerate(urls):
      match = df.index[df['to_scrape'] == urls[i]].tolist()
      mapping_dictionary[i] = match 


  existing_texts = [x[:-4] for x in os.listdir(text_output_folder) if ".DS" not in x]
  to_download = [x for x in range(0, len(urls)) if str(x).zfill(5) not in existing_texts]

  print("Beginning download of {} texts to {}".format(len(to_download), text_output_folder))
  for idx, url in enumerate(to_download[0:]):
    print(idx)
    download_url(url)
  #pool = multiprocessing.Pool(16)
  #zip(*pool.map(download_url, to_download)) 
  #pool.close()
  #pool.join()