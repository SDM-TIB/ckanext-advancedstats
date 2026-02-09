from logging import getLogger

import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
import ckanext.advancedstats.views as views
from ckan.common import config
from ckan.lib.plugins import DefaultTranslation
from ckanext.advancedstats.controller import SELECTED_STATS_KEY

from .tasks import Scheduler, get_value

log = getLogger(__name__)


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


class AdvancedStats(p.SingletonPlugin, DefaultTranslation):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IBlueprint, inherit=True)
    p.implements(p.ITemplateHelpers)
    p.implements(p.ITranslation)

    def __init__(self, *args, **kwargs):
        self.scheduler = Scheduler()
        super().__init__(*args, **kwargs)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_resource('static', 'advancedstats')
        toolkit.add_ckan_admin_tab(config_, 'advancedstats_admin.admin', 'AdvancedStats', icon='chart-line')

        if config_.get(SELECTED_STATS_KEY, None) is None:
            config_[SELECTED_STATS_KEY] = 'datasets organizations groups resources'

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')

        schema.update({
            SELECTED_STATS_KEY: [ignore_missing]
        })

        return schema

    def get_blueprint(self):
        return views.get_blueprints()

    def get_helpers(self):
        return {
            'advanced_stats': get_advanced_site_statistics,
            'kg_triple_icon': get_kg_triple_icon,
            'selected_stats': get_selected_statistics
        }
