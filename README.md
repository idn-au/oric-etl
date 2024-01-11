# ORIC Extract ETL Scripts

ETL Scripts for Indigenous corporation data published by ORIC.  


`etl.py` creates 2 files from `source.csv`.
- `oricAgnets.ttl`
- `industries.ttl`

`oricAgents.ttl` contains the extracted agents for upload to the agentsdb  
`industries.ttl` contains an extracted vocabulary for the types of industries that ORIC agents operate in. for upload to IDN vocprez.

The ORIC data is updated monthly and published [here](https://data.gov.au/data/dataset/aboriginal-and-torres-strait-islander-corporations-oric)


ORIC registered corporations are corporations that comply with the Corporations (Aboriginal and Torres Strait Islander) Act 2006 (CATSI Act).

**The three CATSI Act requirements are:**
- All members must be at least 15 years old.
- Most members must be Aboriginal or Torres Strait Islander.
- By default, you must have at least five members. If you wish to have fewer than five (for example, a sole trader), you can apply for an exemption from that requirement.


## See Also

- [ agentsdb-data ](https://github.com/idn-au/agentsdb-data)
- [ agentsdb-crud-ui ](https://github.com/idn-au/agentsdb-crud-ui)
- [ vocab-data ](https://github.com/idn-au/vocab-data)
- [ spatial-data ](https://github.com/idn-au/spatial-data)
- [ catalogue-data ](https://github.com/idn-au/catalogue-data)
