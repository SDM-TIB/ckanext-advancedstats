from logging import getLogger

import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from SPARQLWrapper import SPARQLWrapper, JSON
from ckan.common import config
from ckan.lib.plugins import DefaultTranslation

from .tasks import Scheduler, get_value

log = getLogger(__name__)

kg_url = config.get('ckanext.advancedstats.kgurl', None)
if kg_url is None:
    sparql = None
else:
    sparql = SPARQLWrapper(config.get('ckanext.advancedstats.kgurl', ''))
    sparql.setReturnFormat(JSON)
    sparql.setQuery('SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }')


def get_advanced_site_statistics():
    return {
        'dataset_count': get_value('ckanext.advancedstats.dataset_count', -1),
        'group_count': get_value('ckanext.advancedstats.group_count', -1),
        'organization_count': get_value('ckanext.advancedstats.organization_count', -1),
        'resource_count': get_value('ckanext.advancedstats.resource_count', -1),
        'jupyter_count': get_value('ckanext.advancedstats.jupyter_count', -1),
        'triples': get_value('ckanext.advancedstats.triples', -1)
    }


class AdvancedStats(p.SingletonPlugin, DefaultTranslation):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers)
    p.implements(p.ITranslation)

    def __init__(self, *args, **kwargs):
        self.scheduler = Scheduler()
        super().__init__(*args, **kwargs)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_resource('static', 'advancedstats')

    def get_helpers(self):
        return {
            'advanced_stats': get_advanced_site_statistics
        }
