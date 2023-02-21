# Python Panthers: Kamath, Sai, Shankar
# Final Project
# Text Analysis

#%%
import os
import datetime as dt

import pandas as pd

import requests
from bs4 import BeautifulSoup

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import show

import spacy
#python -m spacy download en_core_web_sm
from spacytextblob.spacytextblob import SpacyTextBlob
import geonamescache

unparsed_rows = []
text_data = []

for number in range(0, 80, 5):
    
    url = "https://incidentreports.uchicago.edu/incidentReportArchive.php?startDate=1667278800&endDate=1669096800&offset={number}".format(number = number) # having the URL dynamically alter
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    table = soup.find('table')

    for row in table.find_all('tr'):

        td_tags = row.find_all('td')
        unparsed_rows.append([val.text for val in td_tags])

    text_data.append(unparsed_rows) ## appending all the rows (this output needs to be flattened, since it will be a list within a list within a list)

text_data = [text for sublist in text_data for text in sublist] # flattening out our nested list
text_data = [x for x in text_data if x != []] # removing the empty lists

crime, location, date, text = [], [], [], []
for nested in text_data:
    crime.append(nested[0])
    location.append(nested[1])
    date.append(nested[2])
    text.append(nested[4])

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('spacytextblob');

def for_analysis(text):
    doc = nlp(text)
    return round(doc._.blob.polarity, 4), round(doc._.blob.subjectivity, 4)

files_data = pd.DataFrame(zip(crime, location, date, map(for_analysis, text)))
files_data.columns = ['Crime', 'Location', 'Date', 'Analysis']
files_data[['Polarity', 'Subjectivity']] = pd.DataFrame(files_data['Analysis'].tolist(), index=files_data.index)

# Getting Dates columns to graph across time
files_data['Date'] = pd.to_datetime(files_data['Date'])
files_data['Day'] = files_data['Date'].dt.day

files_data = files_data.groupby(['Day']).mean()
files_data = files_data.reset_index()

def make_plot(data, variable):
    fig, ax = plt.subplots()
    fig = sns.lineplot(data, x = 'Day', y = variable)
    ax.set(xlabel = 'Days (Novermber 2022)')
    ax.set_title((f'{variable} of Reported Crime Desriptions'))
    show(fig)
    fig.figure.savefig(f'Text Analysis - Plot - {variable}.png')

variables = ['Polarity', 'Subjectivity']

for variable in variables: 
    make_plot(files_data, variable)

# Citaitons:
#   https://stackoverflow.com/questions/4842956/python-how-to-remove-empty-lists-from-a-list
#   https://stackoverflow.com/questions/67530554/how-to-extract-elements-from-a-nested-list