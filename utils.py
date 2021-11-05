import os
import sys
import pandas as pd
import requests
import json

sys.path.append(os.path.realpath('./src'))
from ena import query_covid_resources

# import plotly.graph_objs as go

def countries_update_df():
    ena_json = _ena_advanced_search_json()

    data = {}
    for record in ena_json:
        country = record['country']
        if ':' in country:
            cspl = country.split(':')
            country = cspl[0]

        try:
            data[country][3] += 1 
        except KeyError:
            data[country] = [country, 0, 0, 1, 'n']

        if record['accession'][:4] == 'SAME':
            data[country][1] += 1
            data[country][4] = 'y'
        else:
            data[country][2] += 1

    try:
        del data['']
    except KeyError:
        pass

    df = pd.DataFrame.from_dict(
            data, orient='index',
            columns=['Country', 'Submissions to DataHubs', 'Submissions to other INSDC sources', 'Total submissions', 'European submitters to DataHubs?']
        )
    df = df.sort_values(by=['Total submissions'], ascending=False)
    return df

def sync_status_df():
    sync_data = {}
    ncbi_seq_count = query_covid_resources.ncbi_count("nucleotide","txid2697049[Organism:noexp]")
    ncbi_read_count = query_covid_resources.ncbi_count("sra","txid2697049[Organism:noexp]")
    sync_data['NCBI'] = ['NCBI', ncbi_seq_count, ncbi_read_count]

    ena_as_seq_count = query_covid_resources.ena_advanced_search_count("sequence", "tax_tree(2697049)")
    ena_as_read_count = query_covid_resources.ena_advanced_search_count("read_experiment", "tax_tree(2697049)")
    sync_data['ENA Advanced Search'] = ['ENA Advanced Search', ena_as_seq_count, ena_as_read_count]

    ebi_search_seq_full = query_covid_resources.ebi_search_count("embl", "TAXONOMY:2697049")
    ebi_search_read_full = query_covid_resources.ebi_search_count("sra-experiment", "TAXONOMY:2697049")
    sync_data['EBI Search (All)'] = ['EBI Search (All)', ebi_search_seq_full, ebi_search_read_full]

    ebi_search_seq_cv19 = query_covid_resources.ebi_search_count("embl-covid19", "id:[* TO *]")
    ebi_search_read_cv19 = query_covid_resources.ebi_search_count("sra-experiment-covid19", "id:[* TO *]")
    sync_data['EBI Search (CV19)'] = ['EBI Search (CV19)', ebi_search_seq_cv19, ebi_search_read_cv19]

    portal_seq_count = query_covid_resources.covid19dataportal_count("sequences")
    portal_read_count = query_covid_resources.covid19dataportal_count("raw-reads")
    sync_data['COVID-19 Data Portal'] = ['COVID-19 Data Portal', portal_seq_count, portal_read_count]

    df = pd.DataFrame.from_dict(
        sync_data, orient='index', columns=['Resource', 'Sequences', 'Raw Reads']
    )
    return df


def slicer(min_date, max_date):
    step = 1
    if 5 < max_date - min_date <= 10:
        step = 2
    elif 10 < max_date - min_date <= 50:
        step = 5
    elif max_date - min_date > 50:
        step = 10
    marks_data = {}
    for i in range(int(min_date), int(max_date) + 1, step):
        if i > int(max_date):
            marks_data[i] = str(int(max_date))
        else:
            marks_data[i] = str(i)

    if i < int(max_date):
        marks_data[int(max_date)] = str(max_date)

    return marks_data

def min_max_date(df):
    min_date = df["collection_date"].min()
    max_date = df["collection_date"].max()
    if min_date > max_date:
        tmp = min_date
        min_date = max_date
        max_date = tmp
    return min_date, max_date
