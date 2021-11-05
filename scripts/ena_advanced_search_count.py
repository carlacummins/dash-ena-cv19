import sys
import argparse
import requests
import json

sys.path.append(os.path.realpath('../src'))
from ena import query_covid_resources`

parser = argparse.ArgumentParser(
    description="""This script queries ENA's advanced search endpoint and returns counts"""
)
parser.add_argument('--type',   help="(optional) result type to query (default:sequence)")
parser.add_argument('--query', help="(optional) search term to apply (default:'tax_tree(2697049)')")
opts = parser.parse_args(sys.argv[1:])

type = "sequence" if not opts.type else opts.type
query = "tax_tree(2697049)" if not opts.query else opts.query

print(query_covid_resources.ena_advanced_search_count(type, query))
