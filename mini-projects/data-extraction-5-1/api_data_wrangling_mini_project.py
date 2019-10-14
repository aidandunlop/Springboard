
# coding: utf-8

# This exercise will require you to pull some data from the Qunadl API. Qaundl is currently the most widely used aggregator of financial market data.

# As a first step, you will need to register a free account on the http://www.quandl.com website.

# After you register, you will be provided with a unique API key, that you should store:

# In[109]:


# Store the API key as a string - according to PEP8, constants are always named in all upper case
API_KEY = '6YnFKMhA_L55gyQL1Jzw'


# Qaundl has a large number of data sources, but, unfortunately, most of them require a Premium subscription. Still, there are also a good number of free datasets.

# For this mini project, we will focus on equities data from the Frankfurt Stock Exhange (FSE), which is available for free. We'll try and analyze the stock prices of a company called Carl Zeiss Meditec, which manufactures tools for eye examinations, as well as medical lasers for laser eye surgery: https://www.zeiss.com/meditec/int/home.html. The company is listed under the stock ticker AFX_X.

# You can find the detailed Quandl API instructions here: https://docs.quandl.com/docs/time-series

# While there is a dedicated Python package for connecting to the Quandl API, we would prefer that you use the *requests* package, which can be easily downloaded using *pip* or *conda*. You can find the documentation for the package here: http://docs.python-requests.org/en/master/ 

# Finally, apart from the *requests* package, you are encouraged to not use any third party Python packages, such as *pandas*, and instead focus on what's available in the Python Standard Library (the *collections* module might come in handy: https://pymotw.com/3/collections/).
# Also, since you won't have access to DataFrames, you are encouraged to us Python's native data structures - preferably dictionaries, though some questions can also be answered using lists.
# You can read more on these data structures here: https://docs.python.org/3/tutorial/datastructures.html

# Keep in mind that the JSON responses you will be getting from the API map almost one-to-one to Python's dictionaries. Unfortunately, they can be very nested, so make sure you read up on indexing dictionaries in the documentation provided above.

# In[110]:


# First, import the relevant modules
import requests
import collections


# In[111]:


# Now, call the Quandl API and pull out a small sample of the data (only one day) to get a glimpse
# into the JSON structure that will be returned
payload = {'api_key': API_KEY, 'start_date': '2019-04-11', 'end_date': '2019-04-11'}
sample_request = requests.get('https://www.quandl.com/api/v3/datasets/FSE/AFX_X/data.json', params=payload)
sample = sample_request.json()


# In[112]:


# Inspect the JSON structure of the object you created, and take note of how nested it is,
# as well as the overall structure
print(sample)


# #### Inspecting the JSON structure
# JSON Response contains data nested under `dataset_data`, with column names and other metadata, followed by a `data` field, containing the actual data. There are some missing entries.

# These are your tasks for this mini project:
# 
# 1. Collect data from the Franfurt Stock Exchange, for the ticker AFX_X, for the whole year 2017 (keep in mind that the date format is YYYY-MM-DD).
# 2. Convert the returned JSON object into a Python dictionary.
# 3. Calculate what the highest and lowest opening prices were for the stock in this period.
# 4. What was the largest change in any one day (based on High and Low price)?
# 5. What was the largest change between any two days (based on Closing Price)?
# 6. What was the average daily trading volume during this year?
# 7. (Optional) What was the median trading volume during this year. (Note: you may need to implement your own function for calculating the median.)

# In[118]:


# PART 1 and 2
payload = {'api_key': API_KEY, 'start_date': '2017-01-01', 'end_date': '2017-12-31'}
request = requests.get('https://www.quandl.com/api/v3/datasets/FSE/AFX_X/data.json', params=payload)
response = request.json()
data_dict = response['dataset_data']
data_dict


# In[114]:


# get column from column name
def getColumn(data, column_name):
    column_index = data['column_names'].index(column_name)
    data = data_dict['data']
    return [row[column_index] for row in data]


# In[115]:


# PART 3
data = data_dict['data']
open_col = getColumn(data_dict, 'Open')
highest = max(x for x in open_col if x is not None)
lowest = min(x for x in open_col if x is not None)
print('Highest:',highest)
print('Lowest:',lowest)


# In[132]:


# subtract list 1 from list 2. If an element is 'None', return NaN.
def diff(list1, list2):
    return [i - j if i is not None and j is not None else float('NaN') for i, j in zip(list1, list2)]


# In[133]:


# PART 4
high_col = getColumn(data_dict, 'High')
low_col = getColumn(data_dict, 'Low')

differences = diff(high_col, low_col)
largest_difference = max(differences)
print("Largest difference: {:.2f}".format(largest_difference))


# In[140]:


# PART 5
# get list of differences between dayB.open and dayA.close for all days (A, B) (excluding start and end)
close_col = getColumn(data_dict, 'Close')
truncated_close = close_col[:-1] # ignore end day 
truncated_open = open_col[1:] # ignore start day
largest_day_difference = max(diff(truncated_open, truncated_close))
print("Largest difference between days: {:.2f}".format(largest_day_difference))


# In[150]:


# PART 6
from statistics import mean 
trading_volume_col = getColumn(data_dict, 'Traded Volume')
print("Average daily trading volume: {:.2f}".format(mean(trading_volume_col)))


# In[152]:


# PART 7
from statistics import median
print("Median daily trading volume: {:.2f}".format(median(trading_volume_col)))


# In[ ]:




