from rdflib import Graph, URIRef
from pyshex import ShExEvaluator
import io

def get_subset(shex, rdf, inputformat="turtle", outputformat="turtle", subsettype="open"):
    graph = Graph()
    graph.parse(data=rdf, format=inputformat)

    # Create a new RDF graph for storing the RDF subset
    new_graph = Graph()

    # ShEx validate

    results = ShExEvaluator().evaluate(rdf, shex)
    for r in results:
        if r.result:
            # Define the URI for which you want to retrieve the outgoing arcs
            uri = URIRef(r.focus)

            # Construct a SPARQL query to retrieve the outgoing arcs of the given URI
            query = """
                SELECT ?predicate ?object
                WHERE {
                    <%s> ?predicate ?object .
                }
            """ % uri

            # Execute the SPARQL query and retrieve the subset of outgoing arcs
            results = graph.query(query)

            # Process the results and add triples to the new graph
            for row in results:
                predicate, obj = row
                new_graph.add((uri, predicate, obj))

            # Print the contents of the new graph

    return new_graph.serialize(format=outputformat, encoding="utf-8").decode("utf-8")