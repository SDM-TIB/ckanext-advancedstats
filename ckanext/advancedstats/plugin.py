from logging import getLogger

import ckan.logic as logic
import ckan.model as model
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from SPARQLWrapper import SPARQLWrapper, JSON
from ckan.common import config
from ckan.lib.plugins import DefaultTranslation

log = getLogger(__name__)

kg_url = config.get('ckanext.advancedstats.kgurl', None)
if kg_url is None:
    sparql = None
else:
    sparql = SPARQLWrapper(config.get('ckanext.advancedstats.kgurl', ''))
    sparql.setReturnFormat(JSON)
    sparql.setQuery('SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }')


def get_advanced_site_statistics():
    stats = {}
    # The following stats are replicated using the logic from CKAN 2.10
    stats['dataset_count'] = logic.get_action('package_search')({}, {"rows": 1})['count']
    stats['group_count'] = len(logic.get_action('group_list')({}, {}))
    stats['organization_count'] = len(logic.get_action('organization_list')({}, {}))

    # The following stats are added by ckanext-advancedstats
    q_res = model.Session.query(model.Resource) \
        .join(model.Package) \
        .filter(model.Package.state == 'active') \
        .filter(model.Package.private == False) \
        .filter(model.Resource.state == 'active') \

    stats['resource_count'] = len(q_res.all())
    stats['jupyter_count'] = len(q_res.filter(getattr(model.Resource, 'url').ilike('%' + '.ipynb')).all())

    if sparql is not None:
        stats['triples'] = 0
        try:
            res = sparql.queryAndConvert()
            for r in res['results']['bindings']:
                stats['triples'] = r['count']['value']
        except Exception:
            pass
    else:
        stats['triples'] = -1
    log.info('The number of triples: ' + str(stats['triples']))
    return stats


class AdvancedStats(p.SingletonPlugin, DefaultTranslation):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers)
    p.implements(p.ITranslation)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_resource('static', 'advancedstats')

    def get_helpers(self):
        return {
            'advanced_stats': get_advanced_site_statistics
        }
