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
                print(".")
                new_graph.add((uri, predicate, obj))

            # Print the contents of the new graph

    return new_graph.serialize(format=outputformat, encoding="utf-8").decode("utf-8")

rdf = """
BASE <http://example.org/ex/>

PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <http://ex.example/#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX : <http://hl7.org/fhir/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
<Patient2>
  :name "Bob" ;
  :birthdate "1999-12-31"^^xsd:date ;
  :has :BloodPressureMeasurementShape .
<BPDate1>
  :date "2010-12-31"^^xsd:date.
<SBP1>
  :valueS 140 .
<DBP1>
  :valueD 90 .
<ABP1>
  :valueA 97 .
<BPMMethod1>
  :method <non-invasive> .
<BPMLocation1>
  :location <arm> .
<BodyPosition1>
  :position <sittingposition> .
<DEP1>
  :type <typeIV>.

<BPM1>
  a :BloodPressureMeasurementShape ;
  rdfs:label "First BP measurement" ;
  :subject  <Patient2> ;
  :hasmeasurementDate <BPDate1> ;
  :valueSBP <SBP1> ;
  :valueDBP <DBP1> ;
  :valueABP <ABP1> ;
  :method <BPMMethod1> ;
  :location <BPMLocation1> ;
  :type <DEP1> ;
  :position <BodyPosition1> .
"""

shex = """
BASE <http://example.org/ex/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <http://ex.example/#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX : <http://hl7.org/fhir/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
start = @<BloodPressureMeasurementShape>
<PatientShape> {                    # A Patient has:
:name xsd:string*;                        #   one or more names
:birthdate xsd:date?   ;          #   and an optional birthdate.
}
<BloodPressureMeasurementShape> {
  rdfs:label  xsd:string ;
  :subject @<PatientShape> ;
  :hasmeasurementDate  @<BPDateShape> ;
  :valueSBP @<SBPvalueShape> ;
  :valueDBP @<DBPvalueShape> ;
  :valueABP @<ABPvalueShape>? ;
  :hasLocation @<BPMeasurementLocationShape>? ;
  :hasType @<DEPShape>? ;
  :isAffectedBy @<BodyPositionShape>?
}
<SBPvalueShape> {
   :valueS  xsd:integer;
}
<DBPvalueShape> {
   :valueD  xsd:integer;
}
<ABPvalueShape> {
   :valueA  xsd:integer;
}
<BPMeasurementMethodShape> {
   :method [<invasive> <non-invasive>];
}
<BPMeasurementInvasiveMethodShape> {
   :method [<invasive>];
}
<BPMeasurementNoninvasiveMethodShape> {
   :method [<non-invasive>];
}
<BPDateShape> {
   :date  xsd:date;
}
<BPMeasurementLocationShape> {
   :location [<arm> <leg> <ankle>];
}
<DEPShape> {
   :type [<typeIV> <typeV>];
}
<BodyPositionShape> {
   :position [<sittingposition> <recumbentbodyposition> <orthostaticbodyposition> <positionwithtilt> <trendelenburgposition>];
}
"""

print(get_subset(shex, rdf))