import sys
import argparse
import requests
import xmltodict

sys.path.append(os.path.realpath('../src'))
from ena import query_covid_resources

parser = argparse.ArgumentParser(
    description="""This script queries EBI Search endpoint and returns counts"""
)
parser.add_argument('--domain', help="(optional) search domain to query (default:embl-covid19)")
parser.add_argument('--query',  help="(optional) search term to apply (default:'id:[* TO *]')")
opts = parser.parse_args(sys.argv[1:])

# domain = "embl" if not opts.domain else opts.domain
# query = "TAXONOMY:2697049" if not opts.query else opts.query
domain = "embl-covid19" if not opts.domain else opts.domain
query = "id:[* TO *]" if not opts.query else opts.query

print(query_covid_resources.ebi_search_count(domain, query))
