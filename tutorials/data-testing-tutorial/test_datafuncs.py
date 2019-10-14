import numpy as np
import datafuncs as dfn
import pytest
import string
import pandas as pd
import yaml

def test_increment():
  assert dfn.increment(2) == 3

def test_min_max_scaler():
  arr = np.array([1, 2, 3])
  result = dfn.min_max_scaler(arr)
  assert np.array_equal(result, np.array([0, 0.5, 1]))
  assert result.min() == 0
  assert result.max() == 1

  with pytest.raises(AssertionError):
    dfn.min_max_scaler(2)
    dfn.min_max_scaler([])
    dfn.min_max_scaler([15])


def test_strip_punctuation():
  text = 'Hello my name is Aidan. Aidan, is my name.'
  without_punc = dfn.strip_punctuation(text)
  assert set(without_punc).isdisjoint(string.punctuation)

def test_bag_of_words():
  text = 'Hello my name is Aidan. Aidan, is my name.'
  bag_of_words = dfn.bag_of_words(text)
  assert len(bag_of_words) ==  5
  assert bag_of_words == set(['Hello', 'my', 'name', 'is', 'Aidan'])

def check_schema(df, meta_columns):
  for col in df.columns:
    assert col in meta_columns, f'"{col}" not in metadata col spec'

def read_metadata(handle):
    with open(handle, 'r+') as f:
        metadata_str = ''.join(l for l in f.readlines())
        return yaml.load(metadata_str, Loader=yaml.FullLoader)

def test_budget_schemas():
  columns = read_metadata('data/metadata_budget.yml')['columns']
  df = pd.read_csv('data/boston_budget.csv')
  check_schema(df, columns)

def test_ei_schemas():
  columns = read_metadata('data/metadata_ei.yml')['columns']
  df = pd.read_csv('data/boston_ei.csv')
  check_schema(df, columns)
