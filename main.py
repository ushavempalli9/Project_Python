import csv
import xml.etree.ElementTree as ET
from datetime import timedelta, date, datetime
import json
import pandas


def update_test_payload_xml(dep, ret):
    file = ET.parse('test_payload1.xml')
    for d in file.iter('DEPART'):
        result = date.today() + timedelta(days=dep)
        d.text = result.strftime('%Y%m%d')

    for r in file.iter('RETURN'):
        result = date.today() + timedelta(days=ret)
        r.text = result.strftime('%Y%m%d')

    file.write('updated_payload1.xml')


def update_json(elem):
    with open('test_payload.json') as json_file:
        data = json.load(json_file)
        if elem in data:
            data.pop(elem)
        else:
            for k, v in data.items():
                if type(v) == dict:
                    v.pop(elem)
        print(data)

    with open('updated_json.json', 'w') as convert_file:
        convert_file.write(json.dumps(data, indent=2))


def read_jmeter(file_name):
    custom_headers = ''
    chunk_size = 10000
    reader = pandas.read_table(file_name, sep="|", header=None, chunksize=chunk_size)
    for index, chunk in enumerate(reader):
        if index == 0:
            chunk.to_csv("out.csv", index=False, sep="|", header=custom_headers)

    with open('out.csv') as f:
        reader = csv.DictReader(f)  # read rows into a dictionary format
        for row in reader:
            for k,v in row.items():
                if k =='responseCode':
                    if v != '200':
                        timestamp = int(row['timeStamp'])
                        date = datetime.utcfromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
                        print(row['label'], row['responseCode'], row['responseMessage'], row['failureMessage'],
                              date)