# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 08:37:39 2021

@author: BOULLI Marouan, MARCAURELIO Hugo
Project : "Internship S6"

Section: "Useful tools to develop"
Subsection: "Second task"
"""


from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import json
import requests

# Create an object that represents the wikidata Sparql query service
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# The keyword contained in labels, description or alias of wikidata resources that we're looking for
keyword = 'chocolate'

# The Sparql query that searches for wikidata resources containing the keyword
query = '''SELECT DISTINCT ?item ?label
WHERE
{
  SERVICE wikibase:mwapi
  {
    bd:serviceParam wikibase:endpoint "www.wikidata.org";
                    wikibase:api "Generator";
                    mwapi:generator "search";
                    mwapi:gsrsearch "''' + keyword + '''"@en;
                    mwapi:gsrlimit "max".
    ?item wikibase:apiOutputItem mwapi:title.
  }
  ?item rdfs:label ?label. FILTER( LANG(?label)="en" )

}'''

# Set the query in the wikidata sparql service
sparql.setQuery(query)
# Set the format of the results in the wikidata sparql service
sparql.setReturnFormat(JSON)
# Generates a Python dictionary
results = sparql.query().convert()
# Returns a dataframe containing the data
results_df = pd.json_normalize(results['results']['bindings'])
# Dataframe with 5 columns : item.type, item.value, label.xml:lang, label.type and label.value
print (list(results_df.columns))
# Print the top of the results
print(results_df[['item.value', 'label.value']].head())

# Write the Uri's in a new file
file = open("results.txt", "w")
for i in range(len(results_df["item.value"])):
    file.write(results_df["item.value"][i])
    file.write("\n")
file.close()




filename = "query.json"
with open(filename, encoding='utf-8') as json_file:
    data = json.load(json_file)
    file = open("results.txt", "w")
    for i in data:
        uri = i.get("item")
        file.write(uri) 
        file.write("\n")
    file.close()


url = 'https://query.wikidata.org/sparql'
query = '''
SELECT DISTINCT ?item ?label
WHERE
{
  SERVICE wikibase:mwapi
  {
    bd:serviceParam wikibase:endpoint "www.wikidata.org";
                    wikibase:api "Generator";
                    mwapi:generator "search";
                    mwapi:gsrsearch "inlabel:Morocco"@en;
                    mwapi:gsrlimit "max".
    ?item wikibase:apiOutputItem mwapi:title.
  }
  ?item rdfs:label ?label. FILTER( LANG(?label)="en" )

}
'''
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()
file = open("results.txt", "w")
for i in data:
        uri = i
        file.write(uri) 
        file.write("\n")
file.close()


