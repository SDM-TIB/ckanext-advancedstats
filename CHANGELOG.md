# Changelog

# v0.6.0 - 2026-02-09
- Add admin panel to configure
  - Statistics to be displayed,
  - Update frequency, and
  - Knowledge graph URL
- Set width of statistics based on the number of statistics displayed
- Refactor code base
- Update German translation

# v0.5.1 - 2026-02-05
- Update German translation

# v0.5.0 - 2026-02-04
- Change icon for groups
- Add active user count
- Add link to datasets containing Jupyter notebooks
- Defer initial update by one minute

# v0.4.2 - 2026-01-30
- Fix issue with missing helper function in older CKAN versions

# v0.4.1 - 2026-01-22
- Fix issue with unreleased locks

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

