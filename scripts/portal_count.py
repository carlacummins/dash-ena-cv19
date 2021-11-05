import sys
import argparse
import requests
import json

sys.path.append(os.path.realpath('../src'))
from ena import query_covid_resources

parser = argparse.ArgumentParser(
    description="""This script queries COVID-19 data portal endpoints and returns counts"""
)
parser.add_argument('--type',   help="(optional) result type to query (default:sequences)")
opts = parser.parse_args(sys.argv[1:])

type = "sequences" if not opts.type else opts.type

print(query_covid_resources.covid19dataportal_count(type))
