from ckanext.advancedstats.controller import AdvancedStatsController
from flask import Blueprint

admin_bp = Blueprint('advancedstats_admin', __name__ + '_admin', url_prefix='/ckan-admin')
admin_bp.add_url_rule('/advancedstats', view_func=AdvancedStatsController.admin, methods=['GET', 'POST'])


def get_blueprints():
    return [admin_bp]
