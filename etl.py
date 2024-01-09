"""
Convert ORIC extract from csv to RDF
"""
from datetime import date

import pandas as pd
from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import RDF, SDO


def main():
    g = Graph()
    dataset_iri = URIRef("https://example.org/oric-extract")
    DS = Namespace(str(dataset_iri) + "/")
    IDNCP = Namespace("https://data.idnau.org/pid/cp/")
    g.bind("idncp", IDNCP)

    g.add((dataset_iri, SDO.dateCreated, Literal(date.today(), datatype=SDO.Date)))

    df = pd.read_csv("oric_corps2023.csv", encoding="ISO-8859-1")
    for index, row in df.iterrows():
        item_iri = URIRef(DS + str(row["ICN"]))
        g.add((dataset_iri, SDO.hasPart, item_iri))
        g.add((item_iri, RDF.type, SDO.Organization))
        if row["Status"] == "Registered":
            g.add(
                (
                    item_iri,
                    SDO.foundingDate,
                    Literal(row["Status Date"], datatype=SDO.Date),
                )
            )
        else:
            g.add(
                (
                    item_iri,
                    SDO.dissolutionDate,
                    Literal(row["Status Date"], datatype=SDO.Date),
                )
            )
        g.add(
            (item_iri, SDO.identifier, Literal(str(row["ABN"]), datatype=IDNCP.abnId))
        )
        g.add((item_iri, SDO.location, Literal(str(row["State"]))))
        g.add((item_iri, SDO.industry, Literal(str(row["Industry"]))))
        g.add((item_iri, SDO.postalCode, Literal(str(row["Post Code"]))))
        g.add((item_iri, SDO.nonprofitStatus, Literal(str(row["ACNC Registered?"]))))
        g.add(
            (
                item_iri,
                SDO.numberOfEmployees,
                Literal(str(row["Numbe of Members"]), datatype=SDO.Number),
            )
        )
        g.add((item_iri, SDO.url, Literal(str(row["URL"]), datatype=SDO.URL)))
    g.serialize(destination='oric.ttl', format="longturtle")


if __name__ == "__main__":
    main()
