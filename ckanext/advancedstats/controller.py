import logging

import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
from ckan.common import request
from ckan.plugins import toolkit

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

SELECTED_STATS_KEY = 'ckanext.advancedstats.stats'


class AdvancedStatsController:

    @staticmethod
    def _check_access():
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user,
            'auth_user_obj': toolkit.c.userobj
        }
        try:
            logic.check_access('sysadmin', context, {})
        except logic.NotAuthorized:
            base.abort(403, toolkit._('Need to be system administrator to administer.'))

    @staticmethod
    def admin():
        AdvancedStatsController._check_access()

        if request.method == 'POST':
            action = request.form.get('action', None)
            if action == 'stats':
                selected_stats_list = request.form.getlist('features')

                if len(selected_stats_list) > 0:
                    selected_stats_string = ' '.join(selected_stats_list)
                    logic.get_action(u'config_option_update')({
                        u'user': toolkit.c.user
                    }, {
                        SELECTED_STATS_KEY: selected_stats_string
                    })
                    toolkit.h.flash_success(toolkit._('Selected statistics has been updated successfully.'))
                else:
                    toolkit.h.flash_error(toolkit._('You need to select at least one statistic to be displayed.'))

        return toolkit.render('admin_advancedstats.jinja2',
                              extra_vars={})
