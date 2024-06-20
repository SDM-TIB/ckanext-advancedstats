[![CKAN](https://img.shields.io/badge/ckan-2.10-orange.svg?style=flat-square)](https://github.com/ckan/ckan/tree/2.10) [![CKAN](https://img.shields.io/badge/ckan-2.9-orange.svg?style=flat-square)](https://github.com/ckan/ckan/tree/2.9)

# Advanced Stats

`ckanext-advancedstats` is a CKAN plugin that adds additional statistics about the CKAN instance to the landing page.

## Installation

As usual for CKAN extensions, you can install `ckanext-fedorkg` as follows:

```bash
git clone git@github.com:SDM-TIB/ckanext-advancedstats.git
pip install -e ./ckanext-advancedstats
pip install -r ./ckanext-advancedstats/requirements.txt
```

After installing the plugin, add `advancedstats` to the plugins in your `ckan.ini`.

## Usage

If you are already displaying the default stats, then `ckanext-advancedstats` is a drop-in replacement, i.e., the plugin will work out-of-the-box and there is nothing you need to do.
In the case you are not yet displaying the stats or you are using a customized landing page, you can add the stats by including the following code in your landing page template.

```
{% block stats %}
  {% snippet 'home/snippets/stats.html' %}
{% endblock %}
```

## Changelog

If you are interested in what has changed, check out the [changelog](CHANGELOG.md).

## License

`ckanext-advancedstats` is licensed under AGPL-3.0, see the [license file](LICENSE).
