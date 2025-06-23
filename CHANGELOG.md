# Changelog

# v0.4.0 - 2025-06-23
- Read values from environment instead of configuration
  - Hence, `CKAN_REDIS_URL` is now read from the environment variables instead of the CKAN configuration
- Use different RDF triple icon based on CKAN version
- Specify compatible dependency versions
- Add capability to update job interval
- Minor changes to the statistics template

# v0.3.0 - 2025-03-07
- Display the time of last update in the user's local timezone

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

