import ckan.plugins.toolkit as toolkit
from ckan.common import config
from ckanext.advancedstats.tasks import get_value

SELECTED_STATS_KEY = 'ckanext.advancedstats.stats'


def get_advanced_site_statistics():
    return {
        'dataset_count': get_value('ckanext.advancedstats.dataset_count', -1),
        'group_count': get_value('ckanext.advancedstats.group_count', -1),
        'organization_count': get_value('ckanext.advancedstats.organization_count', -1),
        'resource_count': get_value('ckanext.advancedstats.resource_count', -1),
        'jupyter_count': get_value('ckanext.advancedstats.jupyter_count', -1),
        'triples': get_value('ckanext.advancedstats.triples', -1),
        'datetime': get_value('ckanext.advancedstats.datetime', '-1'),
        'user_count': get_value('ckanext.advancedstats.user_count', -1)
    }


def get_kg_triple_icon():
    if toolkit.check_ckan_version(min_version='2.10'):
        return 'project-diagram'
    else:
        return 'sitemap'


def get_selected_statistics():
    return config.get(SELECTED_STATS_KEY).split()
