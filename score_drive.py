import csv
import requests
import sys

with open('credit_score_clean.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count=0
    for row in csv_reader:
        if line_count == 0:
            print(row)
            heads = row
            line_count+=1
        else:
            req_data = {heads[i]: row[i] for i in range(1,len(row))}
            print(req_data)
            r = requests.get("http://localhost:4000/credit/model", params=req_data)
            print(r.text)
            line_count+=1
