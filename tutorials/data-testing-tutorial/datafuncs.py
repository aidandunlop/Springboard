import numpy as np
import string
import pandas as pd
import yaml

def increment(x):
  return x + 1

def min_max_scaler(arr):
  assert isinstance(arr, np.ndarray), "arr should be a numpy array"
  assert len(set(arr)) > 1, "arr should have more than 1 unique value"
  return (arr - arr.min()) / (arr.max() - arr.min())

def strip_punctuation(text):
  return text.translate(text.maketrans('', '', string.punctuation))

def bag_of_words(text):
  words = set(strip_punctuation(text).split())
  return words

def autospec(handle):
  df = pd.read_csv(handle)
  columns = list(df)
  filename = handle.split('/')[-1]
  dictionary = { "filename": filename, "columns": columns }
  out_filename = "metadata_" + filename.split('.')[0] + '.yml'
  with open(out_filename, 'w') as outfile:
    yaml.dump(dictionary, outfile, default_flow_style=False)

autospec('data/finaid-applications.csv')