# ORIC Extract ETL Scripts

ETL Scripts for Indegenous corporation data published by ORIC.  
For eventual loading into the AgentsDB


The etl.py script creates 2 files.
- oricAgnets.ttl
- industries.ttl

`oricAgents.ttl` contains the extracted agents for upload to the agentsdb  
`industries.ttl` contains an extracted vocabulary for the types of industries that oric agents operate in. for upload to IDN vocprez.

Source data published here: https://data.gov.au/data/dataset/aboriginal-and-torres-strait-islander-corporations-oric


ORIC registered corporations are corporations that comply with the Corporations (Aboriginal and Torres Strait Islander) Act 2006 (CATSI Act).

**The three CATSI Act requirements are:**
- All members must be at least 15 years old.
- Most members must be Aboriginal or Torres Strait Islander.
- By default, you must have at least five members. If you wish to have fewer than five (for example, a sole trader), you can apply for an exemption from that requirement.


## See Also

- [ AgentsDB-data ](https://github.com/idn-au/agentsdb-data)
- [ AgentsDB-crud-ui ](https://github.com/idn-au/agentsdb-crud-ui)
