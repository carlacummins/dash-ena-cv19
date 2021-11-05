import os
import sys

sys.path.append(os.path.realpath('../src'))
from ena import query_covid_resources

ncbi_count = query_covid_resources.ncbi_count("nucleotide","txid2697049[Organism:noexp]")
ena_as_count = query_covid_resources.ena_advanced_search_count("sequence", "tax_tree(2697049)")
ebi_search_full = query_covid_resources.ebi_search_count("embl", "TAXONOMY:2697049")
ebi_search_cv19 = query_covid_resources.ebi_search_count("embl-covid19", "id:[* TO *]")
portal_count = query_covid_resources.covid19dataportal_count("sequences")

print("NCBI NUCLEOTIDE   : {0}".format(ncbi_count))
print("ENA ADV SEARCH    : {0}".format(ena_as_count))
print("EBI SEARCH (ALL)  : {0}".format(ebi_search_full))
print("EBI SEARCH (CV19) : {0}".format(ebi_search_cv19))
print("COVID-19 PORTAL   : {0}".format(portal_count))
