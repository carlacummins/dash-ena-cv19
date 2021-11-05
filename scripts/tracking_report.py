import sys
import requests
import json

data = []
page = 1
while 1:
    raw_reads_url = 'https://www.covid19dataportal.org/api/backend/viral-sequences/raw-reads?page={0}&size={1}&fields=acc,country'.format(page, 1000)
    rr_response = requests.get(raw_reads_url)
    # print("page # {0}".format(page))
    if rr_response.status_code == 500:
        break
    rr_data = json.loads(rr_response.content)
    for rr_entry in rr_data['entries']:
        acc = rr_entry['fields']['acc'][0]
        try:
            country = rr_entry['fields']['country'][0]
        except IndexError:
            continue # skip if no country
        # print("{0}\t{1}".format(acc, country))
        data.append([acc, country])
    page += 1

print("Got {0} results!".format(len(data)))
