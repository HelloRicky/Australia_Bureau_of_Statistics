# Australia_Bureau_of_Statistics (ABS)

Analysis of ABS 2016 data, the currently version only cover NSW data set.
Main focus on population distribution and Ancestry distribution.

## Python files ##
* analysis.py: use json file to generate cvs file depend on the slected features

## Output directory ##
* json_files: included all the table attributes (up to 41 features) parsed from html pages
  * 2.zip only contains the SSC code (State Suburbs Code) and suburb name
  * 4.zip contains the summary table
  * 41.zip contains all the detail tables
* analysis_result: included the csv file parse from json files and output image from Tableau
  * ancestry_count.csv: data used from 41.zip only
  * people_count.csv: data used from both 4.zip and 41.zip
  * images: output images from Tableau of csv files

## Data Source ##

2016 SSC data were from: http://quickstats.censusdata.abs.gov.au/
* Sample link: http://quickstats.censusdata.abs.gov.au/census_services/getproduct/census/2016/quickstat/SSC10233?opendocument
* Lat and Lon data from:http://stat.abs.gov.au/itt/r.jsp?ABSMaps
