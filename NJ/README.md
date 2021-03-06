
__Shapefiles__

## Sources
Our shapefile was sourced from the Census Bureau's Partnership Files (https://www.census.gov/geo/partnerships/pvs/partnership16v1/st34_nj.html). We used [this script](https://github.com/PrincetonUniversity/gerryspam/blob/master/General/scrape_partnership.py) to scrape each county-specific shapefile and build a state-wide shapefile. 

Election results for 2016 were downloaded from [OpenElections](https://github.com/openelections/openelections-data-nj/blob/master/2016/20161108__nj__general__precinct.csv) on April 24th, named `20161108__nj__general__precinct.csv`. 

Election results for 2016 were downloaded from MEDSL by way of the Harvard Dataverse [(link)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PSKDUJ) on April 1st, 2020. Only Hudson County election results were used from the MEDSL data.

Note that our matched precincts are missing two counties: Burlington and Gloucester. Precinct-level election results were not available for these counties. 

## Variables

* `G16DPRS`: `Democratic votes President`
* `G16DPRS`: `Republican votes President`
* `G16DHOR`: `Democratic votes US House`
* `G16RHOR`: `Republican votes US House`