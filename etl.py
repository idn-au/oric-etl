"""
Convert ORIC extract from csv to RDF
"""
import re
from datetime import date

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef, XSD
from rdflib.namespace import DCTERMS, RDF, RDFS, SDO, SKOS

# define states from ASGS: https://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items
STATE = {
    "ACT": URIRef(
        "http://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items/8"
    ),
    "NSW": URIRef(
        "http://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items/1"
    ),
    "NT": URIRef(
        "http://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items/7"
    ),
    "OTHER": URIRef(
        "http://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items/9"
    ),
    "OUTSIDE": URIRef(
        "http://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items/Z"
    ),
    "QLD": URIRef(
        "http://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items/3"
    ),
    "SA": URIRef(
        "http://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items/4"
    ),
    "TAS": URIRef(
        "http://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items/6"
    ),
    "VIC": URIRef(
        "http://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items/2"
    ),
    "WA": URIRef(
        "http://asgs.linked.fsdf.org.au/dataset/asgsed3/collections/STE/items/5"
    ),
}


def strToCamel(string: str) -> str:
    """Convert the given string to camelCase stripping out any non-alphanumeric characters"""
    clean = re.sub(r"[^\w\s]", " ", string).strip()
    words = clean.split(" ")
    return "".join([words[0].lower()] + [word.title() for word in words[1:]])


def extract_vocab(
    column: pd.Series,
    cs_iri: URIRef,
    cs_definition: str,
    creator_iri: URIRef,
    creator_name: str,
    creator_url: str,
    vocab_name: str,
    nested: bool = False,
    seperator: str = "",
    format: str = "longturtle",
    filename: str = "vocab.ttl",
) -> dict:
    """Extract vocab terms from the distinct items given in column

    The parsed vocab is written to disk in the given format (default: longturtle).
    A dictionary of the extracted terms is returned


    :param column: A pandas series containing values to be parsed into a vocab
    :param cs_iri: IRI for the vocabulary to be created
    :param cs_definition: definition of the vocabulary to be created.
    :param creator_iri: IRI of the creator. should be person or organization
    :param creator_name: Name of the vocabulary creator
    :param creator_url: URL for the creator
    :param vocab_name: name of the vocabulary.
    :param nested: Are the values in each cell of the column themselves a list?
    :param seperator: The charactre used to seperate the entries of each cell in column.
                      only required if nested is True.
    :param format: RDF format to use. defaults to longturtle
    :param filename: name of the file to write the vocab to
    """
    g = Graph()
    cs = Namespace(cs_iri)
    g.bind("cs", cs)

    # set up the CS
    g.add((cs_iri, RDF.type, SKOS.ConceptScheme))
    g.add(
        (
            cs_iri,
            DCTERMS.provenance,
            Literal(f"Extracted for {creator_name} {date.today().year}"),
        )
    )
    g.add(
        (
            cs_iri,
            SKOS.definition,
            Literal(cs_definition),
        )
    )
    g.add((cs_iri, DCTERMS.created, Literal(date.today(), datatype=XSD.date)))
    g.add((cs_iri, DCTERMS.modified, Literal(date.today(), datatype=XSD.date)))
    g.add((cs_iri, DCTERMS.publisher, creator_iri))
    g.add((cs_iri, DCTERMS.creator, creator_iri))
    g.add((cs_iri, DCTERMS.rights, Literal("(c) Indigenous Data Network, 2022")))
    g.add((cs_iri, SKOS.prefLabel, Literal(vocab_name)))
    g.add((creator_iri, RDF.type, SDO.Organization))
    g.add((creator_iri, SDO.name, Literal(creator_name)))
    g.add((creator_iri, SDO.url, Literal(creator_url, datatype=XSD.anyURI)))

    concept_set = set()
    for cell in column:
        if not pd.isna(cell):
            if nested:
                values = str(cell).split(seperator)
                for value in values:
                    concept_set.add(str(value).strip())
            else:
                concept_set.add(str(cell).strip())

    concept_dict: dict[str, URIRef] = {}
    for concept in concept_set:
        concept_iri = URIRef(cs_iri + strToCamel(concept))
        g.add((concept_iri, RDF.type, SKOS.Concept))
        g.add((concept_iri, SKOS.prefLabel, Literal(concept)))
        g.add(
            (
                concept_iri,
                SKOS.definition,
                Literal(f"Member of {vocab_name}"),
            )
        )
        g.add((concept_iri, RDFS.isDefinedBy, cs_iri))
        g.add((concept_iri, SKOS.inScheme, cs_iri))
        g.add((cs_iri, SKOS.hasTopConcept, concept_iri))
        concept_dict[strToCamel(concept)] = concept_iri
    g.serialize(destination=filename, format=format)
    return concept_dict


def main():
    g = Graph()
    dataset_iri = URIRef("https://data.idnau.org/pid/agent/oric/")
    DS = Namespace(dataset_iri)
    IDNCP = Namespace("https://data.idnau.org/pid/cp/")
    IDNI = Namespace("https://data.idnau.org/pid/vocab/org-indigeniety/")
    g.bind("idncp", IDNCP)
    g.bind("idni", IDNI)
    g.bind("oricAgents", DS)

    g.add((dataset_iri, SDO.dateCreated, Literal(date.today(), datatype=XSD.Date)))
    g.add((dataset_iri, RDF.type, SDO.Dataset))
    g.add((dataset_iri, SDO.name, Literal("ORIC Extract")))

    df = pd.read_csv("source.csv", encoding="ISO-8859-1")

    # extract industries into a vocab
    industry_vocab = extract_vocab(
        column=df["Industry"],
        cs_iri=URIRef("https://data.idnau.org/pid/vocab/oric/"),
        cs_definition="Industry that an organisation or individual operates in",
        creator_iri=URIRef("https://linked.data.gov.au/org/idn"),
        creator_name="Indigenous Data Network",
        creator_url="https://www.idnau.org",
        vocab_name="ORIC Industry Vocabulary",
        nested=True,
        seperator=";",
        filename='outputs/oricIndustries.ttl'
    )
    for index, row in df.iterrows():
        item_iri = URIRef(DS + strToCamel(row["Corporation"]))

        # set standard properties
        g.add((dataset_iri, SDO.hasPart, item_iri))
        g.add((item_iri, RDF.type, SDO.Organization))
        g.add((item_iri, SDO.name, Literal(row["Corporation"])))
        g.add((item_iri, SDO.description, Literal("ORIC Registered Corporation")))
        g.add((item_iri, DCTERMS.type, IDNI["indigenous-persons-organisation"]))

        # read properties from cells
        g.add((item_iri, SDO.identifier, Literal(row["ICN"], datatype=IDNCP.ICN)))
        if row["Status"] == "Registered":
            g.add(
                (
                    item_iri,
                    SDO.foundingDate,
                    Literal(row["Status Date"], datatype=XSD.Date),
                )
            )
        else:
            g.add(
                (
                    item_iri,
                    SDO.dissolutionDate,
                    Literal(row["Status Date"], datatype=XSD.Date),
                )
            )
        if not pd.isna(row["ABN"]):
            g.add(
                (item_iri, SDO.identifier, Literal(str(row["ABN"]), datatype=IDNCP.abnId))
            )
        if not pd.isna(row["State"]):
            g.add((item_iri, SDO.location, STATE[str(row["State"])]))
        if not pd.isna(row["Industry"]):
            for industries in row["Industry"].split(";"):
                if isinstance(industries, str):
                    g.add(
                        (item_iri, SDO.industry, industry_vocab[strToCamel(industries)])
                    )
                else:
                    for industry in industries:
                        g.add(
                            (
                                item_iri,
                                SDO.industry,
                                industry_vocab[strToCamel(industry)],
                            )
                        )
        if not pd.isna(row["Post Code"]):
            g.add((item_iri, SDO.postalCode, Literal(str(row["Post Code"]))))
        if not pd.isna(row["ACNC Registered?"]):
            g.add((item_iri, SDO.nonprofitStatus, Literal(True, datatype=XSD.boolean)))
        if not pd.isna(row["Numbe of Members"]):
            g.add(
                (
                    item_iri,
                    SDO.numberOfEmployees,
                    Literal(str(row["Numbe of Members"]), datatype=SDO.Number),
                )
            )
        if not pd.isna(row["URL"]):
            g.add((item_iri, SDO.url, Literal(str(row["URL"]), datatype=XSD.anyURI)))
    g.serialize(destination="outputs/oricAgents.ttl", format="longturtle")


if __name__ == "__main__":
    main()
