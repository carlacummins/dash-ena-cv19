import sys, os
import argparse
import requests
import json
import xmltodict
import time

def ncbi(db, term):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={0}&term={1}".format(db, term)
    response = requests.get(url)
    data = xmltodict.parse(response.content)
    return data

def ncbi_count(db, term):
    data = ncbi(db, term)
    return data['eSearchResult']['Count']

def ebi_search(domain, query):
    url = "http://www.ebi.ac.uk/ebisearch/ws/rest/{0}?query={1}".format(domain, query)
    response = requests.get(url)
    data = xmltodict.parse(response.content)
    return data

def ebi_search_count(domain, query):
    data = ebi_search(domain, query)
    return data['result']['hitCount']

# use some rudimentary caching for advanced search as it is slow
def _generate_json_file(json_file):
    type = 'read_experiment'
    query = 'tax_tree(2697049)'
    url = "https://www.ebi.ac.uk/ena/portal/api/search?result={0}&query={1}&fields=accession,country,collection_date,first_public&format=json&limit=0".format(type, query)
    response = requests.get(url)
    data = json.loads(response.content)
    with open(json_file, 'w') as outfile:
        json.dump(data, outfile)

def _ena_advanced_search_json():
    json_file = 'data/country_updates.ena.json'

    # regenerate file if it doesn't exist or is older than 3 hour
    if ( os.path.isfile(json_file) ):
        # print("JSON file exists - checking its age")
        time_in_secs = time.time() - (60 * 60 * 3)  # 3 hours
        stat = os.stat(json_file)
        if stat.st_mtime <= time_in_secs:
            # print("---> file older than 3 hours - regenerating")
            _generate_json_file(json_file)
    else:
        # print("JSON file does not exist - generating")
        _generate_json_file(json_file)

    with open(json_file, 'r') as json_fh:
        return json.load(json_fh)

def ena_advanced_search(type, query):
    return _ena_advanced_search_json()
    # url = "https://www.ebi.ac.uk/ena/portal/api/search?result={0}&query={1}&fields=accession,country&format=json&limit=0".format(type, query)
    # response = requests.get(url)
    # data = json.loads(response.content)
    # return data

def ena_advanced_search_count(type, query):
    data = ena_advanced_search(type, query)
    return len(data)

def covid19dataportal(type, page, size):
    url = "https://www.covid19dataportal.org/api/backend/viral-sequences/{0}?page={1}&size={2}".format(type, page, size)
    response = requests.get(url)
    data = json.loads(response.content)
    return data

def covid19dataportal_count(type):
    data = covid19dataportal(type, 1, 1)
    return data['hitCount']

def query_era(sql):
    era_conn = _setup_connection("ora-vm-069.ebi.ac.uk", 1541, "ERAREAD")
    cursor = era_conn.cursor()
    return cursor.execute(sql)

def query_ena(sql):
    ena_conn = _setup_connection("ora-vm5-008.ebi.ac.uk", 1531, "ENAPRO")
    cursor = ena_conn.cursor()
    return cursor.execute(sql)

def _setup_connection(server, port, service_name):
    oracle_usr, oracle_pwd = get_oracle_usr_pwd()
    client_lib_dir = os.getenv('ORACLE_CLIENT_LIB')
    if not client_lib_dir or not os.path.isdir(client_lib_dir):
        sys.stderr.write("ERROR: Environment variable $ORACLE_CLIENT_LIB must point at a valid directory\n")
        exit(1)
    cx_Oracle.init_oracle_client(lib_dir=client_lib_dir)
    connection = None
    try:
        dsn = cx_Oracle.makedsn(server, port, service_name=service_name)
        connection = cx_Oracle.connect(oracle_usr, oracle_pwd, dsn, encoding="UTF-8")
        return connection
    except cx_Oracle.Error as error:
        print(error)
