[![CKAN](https://img.shields.io/badge/ckan-2.10-orange.svg?style=flat-square)](https://github.com/ckan/ckan/tree/2.10) [![CKAN](https://img.shields.io/badge/ckan-2.9-orange.svg?style=flat-square)](https://github.com/ckan/ckan/tree/2.9)

# Advanced Stats

`ckanext-advancedstats` is a CKAN plugin that adds additional statistics about the CKAN instance to the landing page.
Currently, the plugin displays the following statistics:

- number of datasets
- number of active users
- number of organizations
- number of groups
- number of resources
- number of Jupyter notebooks
- number of RDF triples

The number of RDF triples corresponds to the number of triples in the knowledge graph serving the metadata of the CKAN instance.
Such a knowledge graph can be maintained with the extension `ckanext-kgcreation` [(https://github.com/SDM-TIB/ckanext-kgcreation)](https://github.com/SDM-TIB/ckanext-kgcreation).

## Installation

As usual for CKAN extensions, you can install `ckanext-advancedstats` as follows:

```bash
git clone git@github.com:SDM-TIB/ckanext-advancedstats.git
pip install -e ./ckanext-advancedstats
pip install -r ./ckanext-advancedstats/requirements.txt
```

After installing the plugin, add `advancedstats` to the plugins in your `ckan.ini`.

## Configuration Options

- `ckanext.advancedstats.stats` the statistics to display in the main page
  - Default: `datasets organizations groups resources`
- `ckanext.advancedstats.updatefrequency` the update frequency in minutes
  - Default: `30`
  - For backwards compatibility, the default can also be set with the environment variable `CKANEXT__ADVANCEDSTATS__INTERVAL`, e.g.:
    ```bash
    CKANEXT__ADVANCEDSTATS__INTERVAL=30
    ```
- `ckanext.advancedstats.kg` to include the number of RDF triples in the knowledge graph containing the metadata of your CKAN instance
  - For backwards compatibility, this can also be set with the environment variable `CKANEXT__ADVANCEDSTATS__KGURL`, e.g.:
    ```bash
    CKANEXT__ADVANCEDSTATS__KGURL=https://www.your-site.tld/kg/sparql
    ```

The configuration options mentioned above can also be configured using the admin interface provided by the extension.

The connection string for Redis is read from the CKAN configuration option `CKAN_REDIS_URL` which should already be set in most CKAN instances.

## Usage

If you are already displaying the default stats, then `ckanext-advancedstats` is a drop-in replacement, i.e., the plugin will work out-of-the-box and there is nothing you need to do.
In the case you are not yet displaying the stats, or you are using a customized landing page, you can add the stats by including the following code in your landing page template.

```
{% block stats %}
  {% snippet 'home/snippets/stats.html' %}
{% endblock %}
```

## Changelog

If you are interested in what has changed, check out the [changelog](CHANGELOG.md).

## License

`ckanext-advancedstats` is licensed under AGPL-3.0, see the [license file](LICENSE).

