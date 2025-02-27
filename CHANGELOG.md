# Changelog

# v0.2.0 - 2025-02-27
- Add number of knowledge graph triples
- Store the statistics in Redis
- Scheduled task for updating the statistics, default every 30 minutes 
- Add time of last update
- Add configuration options
  - environment variable `CKANEXT__ADVANCEDSTATS__KGURL` for setting the URL of the knowledge graph
  - environment variable `CKANEXT__ADVANCEDSTATS__INTERVAL` for setting the update interval in minutes
  - CKAN configuration option `CKAN_REDIS_URL` for specifying the Redis connection string

# v0.1.0 - 2024-06-20
- First version, including the following statistics
  - number of datasets
  - number of organizations
  - number of groups
  - number of resources
  - number of Jupyter notebooks

