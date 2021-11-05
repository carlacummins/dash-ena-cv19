import sys
import argparse
import requests
import xmltodict

sys.path.append(os.path.realpath('../src'))
from ena import query_covid_resources

parser = argparse.ArgumentParser(
    description="""This script queries NCBI's eutils search endpoint and returns counts"""
)
parser.add_argument('--db',   help="(optional) NCBI database to query (default:nucleotide)")
parser.add_argument('--term', help="(optional) search term to apply (default:'txid2697049[Organism:noexp]')")
opts = parser.parse_args(sys.argv[1:])

db = "nucleotide" if not opts.db else opts.db
term = "txid2697049[Organism:noexp]" if not opts.term else opts.term

print(query_covid_resources.ncbi_count(db, term))
