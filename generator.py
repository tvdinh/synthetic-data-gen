from pandas import DataFrame, Series
import pandas as pd
import sys
import random as rd
from datetime import datetime, date
import dateparser

# how to take argument <==>, you can certainly be able to write it in Java regardless.

class Field:
    def __init__(self, field_name='name', field_type='string', range='range'):
        self.field_name = field_name
        self.field_type = field_type
        self.range = range

args = sys.argv
if len(args) != 3:
    print("Expected 2 arguments: <config_file> <sample_size>. E.g ./generator.py config.txt 1000")
    exit(1)

config_file = args[1]
print("Config file is: %s." % config_file)
sample_size = int(args[2])
print("Sample size is: %d." % sample_size)

config = pd.read_csv('config.txt', sep=r'\s*,\s*', engine='python') # to trim leading and trailing spaces between field

fields = []
for row in config.values:
    fields.append(Field(row[0],row[1],row[2]))
print(fields)


last_names = pd.read_csv('data/last-names.txt', names=['name'])['name'].values
first_names = pd.read_csv('data/yob2019.txt', names=['name', 'gender', 'count'])['name'].values

def generate_data(field : Field) -> str:
    if field.field_type.lower() == 'number':
        #then you need a range
        lower = float(field.range.split('-')[0])
        upper = float(field.range.split('-')[1])
        return str(round(rd.uniform(lower, upper),2))
    elif field.field_type.lower() == 'full_name':
        return ' '.join((str(first_names[rd.randint(0,len(first_names)-1)]), str(last_names[rd.randint(0,len(last_names)-1)])))
    elif field.field_type.lower() == 'string':
        return "Random description"
    elif field.field_type.lower() == 'datetime':
        lower = dateparser.parse(field.range.split(':')[0]).timestamp() # timestamp of the lower date
        upper = dateparser.parse(field.range.split(':')[1]).timestamp() # timestamp of the upper date
        ts = round(rd.uniform(lower,upper), 0)
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S")
    else:
        # assume string
        return "Random description"

#open the file, write a chunk of 1000 samples to a file as a time.
with open('output.txt','w') as f:
    chunk  = []
    for i in range (0,sample_size):
        record = []
        for field in fields:
            record.append(generate_data(field))
        chunk.append(', '.join(record))
    for i in range (0,sample_size):
        f.write(chunk[i] + "\n")   