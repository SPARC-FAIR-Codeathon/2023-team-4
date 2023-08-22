"""
SPARQL query related functions
Adapted from: 
https://github.com/SciCrunch/sparc-curation/blob/master/docs/sckan-python.ipynb
"""
import io
import csv
import requests
from urllib.parse import quote as url_quote

def procq(res):
    _, (str_count,) = res
    return int(str_count)

def sparql_query(query, *, endpoint, **kwargs):
    qq = url_quote(query, safe='')
    url = f'{endpoint}?query={qq}'
    headers = {'Accept': 'text/csv'}
    resp = requests.get(url, headers=headers)
    return list(csv.reader(io.StringIO(resp.text)))


example_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?A ?Region_A ?B ?Region_B ?C ?Region_C ?Species ?Species_link
{{

    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                ilxtr:hasAxonLocation ?C;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.

    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Neuron_IRI ?Region_A ?Region_B ?Region_C ?Species
"""

unique_species_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?Species
{{
    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B.
    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
}}
ORDER BY ?Species
"""

unique_regionsA_species_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?Region_A
{{
    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                ilxtr:isObservedInSpecies ?Species_link.
    
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    
    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Region_A
"""

unique_regionsB_species_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?Region_B
{{
    ?Neuron_IRI rdfs:label ?Neuron_Label;
                (ilxtr:hasAxonLocation | ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B;
                ilxtr:isObservedInSpecies ?Species_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Region_B
"""

unique_regionsC_species_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?Region_C
{{
    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasAxonLocation ?C;
                ilxtr:isObservedInSpecies ?Species_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Region_C
"""

unique_combined_regions_species_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?Region
{
    {
        ?Neuron_IRI rdfs:label ?Neuron_Label;
                    ilxtr:hasSomaLocation ?A;
                    ilxtr:isObservedInSpecies ?Species_link.

        ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

        ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region.

        FILTER (str(?Species) = "{species_param}")
    }
    UNION
    {
        ?Neuron_IRI rdfs:label ?Neuron_Label;
                    (ilxtr:hasAxonLocation | ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B;
                    ilxtr:isObservedInSpecies ?Species_link.

        ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

        ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region.

        FILTER (str(?Species) = "{species_param}")
    }
    UNION
    {
        ?Neuron_IRI rdfs:label ?Neuron_Label;
                    ilxtr:hasAxonLocation ?C;
                    ilxtr:isObservedInSpecies ?Species_link.

        ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

        ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region.

        FILTER (str(?Species) = "{species_param}")
    }
}
ORDER BY ?Region
"""

combined_regions_all_species_without_synonyms_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Region_URI ?Region
{{

    ?Neuron_IRI (ilxtr:hasSomaLocation | ilxtr:hasAxonLocation | ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?Region_URI. 
    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.

    ?Region_URI rdfs:label ?Region.
}}
ORDER BY ?Region_URI ?Region
"""

combined_regions_all_species_with_synonyms_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Region_URI ?Region
{{

    ?Neuron_IRI (ilxtr:hasSomaLocation | ilxtr:hasAxonLocation | ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?Region_URI. 
    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.

    ?Region_URI (rdfs:label | oboInOwl:hasExactSynonym) ?Region.
}}
ORDER BY ?Region_URI ?Region
"""

# old query; better alternatives available above
unique_combined_regions_all_species_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?Region
{
    {
        ?Neuron_IRI rdfs:label ?Neuron_Label;
                    ilxtr:hasSomaLocation ?A;
                    ilxtr:isObservedInSpecies ?Species_link.

        ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

        ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region.
    }
    UNION
    {
        ?Neuron_IRI rdfs:label ?Neuron_Label;
                    (ilxtr:hasAxonLocation | ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B;
                    ilxtr:isObservedInSpecies ?Species_link.

        ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

        ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region.
    }
    UNION
    {
        ?Neuron_IRI rdfs:label ?Neuron_Label;
                    ilxtr:hasAxonLocation ?C;
                    ilxtr:isObservedInSpecies ?Species_link.

        ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

        ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region.
    }
}
ORDER BY ?Region
"""

neuron_path_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?A ?Region_A ?B ?Region_B ?C ?Region_C ?Species ?Species_link
{{

    ?Neuron_IRI rdfs:label ?Neuron_Label;
                ilxtr:hasSomaLocation ?A;
                ilxtr:hasAxonLocation ?C;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.

    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.

    FILTER (str(?Species) = "{species_param}")
}}
ORDER BY ?Neuron_IRI ?Region_A ?Region_B ?Region_C ?Species
"""

neuron_path_phenotype_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?Species ?phenotype ?A ?B ?C ?Region_A ?Region_B ?Region_C
{

    ?Neuron_IRI rdfs:label ?Neuron_Label.

    ?Neuron_IRI rdfs:label ?Neuron_Label;
                    ilxtr:hasSomaLocation ?A;
                    ilxtr:hasAxonLocation ?C;
                    (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Neuron_IRI ilxtr:hasNeuronalPhenotype ?phenotype_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?phenotype_link (rdfs:label | oboInOwl:hasExactSynonym) ?phenotype.
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.

}
ORDER BY ?Neuron_IRI ?Neuron_Label ?Species ?phenotype ?A ?B ?C ?Region_A ?Region_B ?Region_C
"""

neuron_circuit_role_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?Species ?phenotype ?A ?B ?C ?Region_A ?Region_B ?Region_C
{

    ?Neuron_IRI rdfs:label ?Neuron_Label.

    ?Neuron_IRI rdfs:label ?Neuron_Label;
                    ilxtr:hasSomaLocation ?A;
                    ilxtr:hasAxonLocation ?C;
                    (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Neuron_IRI ilxtr:hasCircuitRole ?phenotype_link.

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    ?phenotype_link (rdfs:label | oboInOwl:hasExactSynonym) ?phenotype.
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.

}
ORDER BY ?Neuron_IRI ?Neuron_Label ?Species ?phenotype ?A ?B ?C ?Region_A ?Region_B ?Region_C
"""

projection_fibres_query = """
SELECT DISTINCT ?Neuron_1_IRI ?Neuron_1_Label
                ?Neuron_2_IRI ?Neuron_2_Label ?Species
WHERE
{
    ?Neuron_1_IRI ilxtr:hasSomaLocation ?Neuron_1_A;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?Neuron_1_B .

    ?Neuron_2_IRI ilxtr:hasSomaLocation ?Neuron_2_A;
                (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ??Neuron_2_B .

    ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    ?Neuron_1_IRI ilxtr:hasForwardConnection ?Neuron_2_IRI .

    ?Neuron_1_IRI rdfs:label ?Neuron_1_Label .
    ?Neuron_2_IRI rdfs:label ?Neuron_2_Label .

    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
}
"""

app_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX partOf: <http://purl.obolibrary.org/obo/BFO_0000050>
PREFIX ilxtr: <http://uri.interlex.org/tgbugs/uris/readable/>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> 

SELECT DISTINCT ?Neuron_IRI ?Neuron_Label ?A ?Region_A ?B ?Region_B ?C ?Region_C ?Species ?Species_link
{

   ?Neuron_IRI rdfs:label ?Neuron_Label;
               ilxtr:hasSomaLocation ?A;
               ilxtr:hasAxonLocation ?C;
              (ilxtr:hasAxonTerminalLocation | ilxtr:hasAxonSensoryLocation) ?B. 
   
   ?Neuron_IRI ilxtr:isObservedInSpecies/rdfs:label ?Species.
   ?Neuron_IRI ilxtr:isObservedInSpecies ?Species_link.
    
    ?A (rdfs:label | oboInOwl:hasExactSynonym) ?Region_A.
    ?B (rdfs:label | oboInOwl:hasExactSynonym) ?Region_B.
    ?C (rdfs:label | oboInOwl:hasExactSynonym) ?Region_C.
    ?Species_link (rdfs:label | oboInOwl:hasExactSynonym) ?Species.
    
}
ORDER BY ?Neuron_IRI ?Region_A ?Region_B ?Region_C ?Species
"""