from pyshex.shex_evaluator import evaluate_cli as shexeval
from pyshex import shex_evaluator
from sparqlslurper import SlurpyGraph

from pyshex.user_agent import SlurpyGraphWithAgent
permagraph = None

def persistent_slurper(rdf: str, *args, **kwargs) -> SlurpyGraph:
    global permagraph
    permagraph = SlurpyGraphWithAgent(rdf, *args, **kwargs)
    return permagraph

def get_sparql_subset(shex, sparql, endpoint, start, output="turtle", subsettype="open"):
    shex_evaluator.SlurpyGraphWithAgent = persistent_slurper
    x = ["-ss",
         "-s", start,
         "-sq", sparql,
         endpoint,
         shex,
         "-ps"]
    shexeval(x)
    print()
    print("RESULT Graph:")
    print(permagraph.serialize(format=output).decode())


sparql_query = """
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>

SELECT * WHERE {
   ?item wdt:P699 ?doid .
}
"""
shex = "https://raw.githubusercontent.com/kg-subsetting/biohackathon2020/main/use_cases/genewiki/genewiki.shex"
get_sparql_subset(shex, sparql_query, "https://query.wikidata.org/sparql", "http://www.wikidata.org/entity/Q12136", subsettype="open")
# shexeval(['-h'])

