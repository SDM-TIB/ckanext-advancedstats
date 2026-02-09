import os
from logging import getLogger

import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
import ckanext.advancedstats.helpers as helpers
import ckanext.advancedstats.views as views
from ckan.lib.plugins import DefaultTranslation
from ckanext.advancedstats.helpers import SELECTED_STATS_KEY, UPDATE_FREQUENCY_KEY, KG_URL_KEY
from ckanext.advancedstats.tasks import Scheduler

log = getLogger(__name__)


class AdvancedStats(p.SingletonPlugin, DefaultTranslation):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IBlueprint, inherit=True)
    p.implements(p.ITemplateHelpers)
    p.implements(p.ITranslation)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduler = None  # init after config has been set

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_resource('static', 'advancedstats')
        toolkit.add_ckan_admin_tab(config_, 'advancedstats_admin.admin', 'AdvancedStats', icon=helpers.icon())

        if config_.get(SELECTED_STATS_KEY, None) is None:
            config_[SELECTED_STATS_KEY] = 'datasets organizations groups resources'
        if config_.get(UPDATE_FREQUENCY_KEY, None) is None:
            freq = os.getenv('CKANEXT__ADVANCEDSTATS__INTERVAL', None)
            if freq is not None:
                config_[UPDATE_FREQUENCY_KEY] = freq
            else:
                config_[UPDATE_FREQUENCY_KEY] = 30
        if config_.get(KG_URL_KEY, None) is None:
            kg_url = os.getenv('CKANEXT__ADVANCEDSTATS__KGURL', None)
            if kg_url is not None:
                config_[KG_URL_KEY] = kg_url

        self.scheduler = Scheduler()

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')

        schema.update({
            SELECTED_STATS_KEY: [ignore_missing],
            UPDATE_FREQUENCY_KEY: [ignore_missing],
            KG_URL_KEY: [ignore_missing]
        })

        return schema

    def get_blueprint(self):
        return views.get_blueprints()

    def get_helpers(self):
        return {
            'advanced_stats': helpers.get_advanced_site_statistics,
            'kg_triple_icon': helpers.get_kg_triple_icon,
            'selected_stats': helpers.get_selected_statistics,
            'stat_width': helpers.width
        }
