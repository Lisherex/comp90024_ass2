# comp90024_ass2
For UniMelb COMP90051-Cluster and Cloud Computing Assignment 2

Assignment Guide (GitLab): https://gitlab.unimelb.edu.au/feit-comp90024/comp90024

Data: 
1. air quality (PM2.5) vs weathere (wind/rainfall)
2. air quality vs COPD：chronic obstructive pulmonary disease
3. air quality vs house price
3. air quality vs vehicle



URL:

|            Name           | Method |                 URL                | Ingress | Path                               | Namespace | Description                                   |
|:-------------------------:|:------:|:----------------------------------:|---------|------------------------------------|-----------|-----------------------------------------------|
| airquality-copd           | [GET]  | /airquality/copd                   | true    | /airquality/copd                   | default   |                                               |
| airquality-houseprice     | [GET]  | /airquality/houseprice             | true    | /airquality/houseprice             | default   |                                               |
| airquality-rsd            | [GET]  | /airquality/rsd                    | true    | /airquality/rsd                    | default   |                                               |
| airquality-vehicle        | [GET]  | /houseprice/copd                   | true    | /houseprice/copd                   | default   |                                               |
| houseprice-copd           | [GET]  | /houseprice/copd                   | true    | /houseprice/copd                   | default   |                                               |
| post-json-data-from-local | [POST] | /post-json-data-from-local/{index} | false   | /post-json-data-from-local/{index} | default   | Upload json data from local to ElasticSearch. |
| update-airquality         | [PUT]  | /update-airquality                 | false   | /update-airquality                 | default   | Update Air Quality Station data from EPA.     |
