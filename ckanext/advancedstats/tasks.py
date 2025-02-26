from datetime import datetime, timedelta
from logging import getLogger
from urllib.parse import urlparse

import ckan.logic as logic
import ckan.model as model
import redis
from SPARQLWrapper import SPARQLWrapper, JSON
from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from ckan.common import config

log = getLogger(__name__)
redis_url = config.get('CKAN_REDIS_URL', 'redis://localhost:6379/0')
redis_client = redis.from_url(redis_url)

kg_url = config.get('ckanext.advancedstats.kgurl', None)
if kg_url is None:
    sparql = None
else:
    sparql = SPARQLWrapper(config.get('ckanext.advancedstats.kgurl', ''))
    sparql.setReturnFormat(JSON)
    sparql.setQuery('SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }')

interval = int(config.get('ckanext.advancedstats.interval', 30))


def store_value(key, value):
    try:
        redis_client.set(key, value)
        log.debug(f"Stored key-value pair in Redis: {key} -> {value}")
    except Exception as e:
        log.error(f"Error storing value in Redis: {e}")


def get_value(key, default_value=None):
    try:
        value = redis_client.get(key)
        if value is not None:
            value = value.decode('utf-8')  # Decode the byte string to a regular string
            log.debug(f"Retrieved from Redis: {key} -> {value}")
            return value
        else:
            log.debug(f"Key not found in Redis: {key}")
            return default_value
    except Exception as e:
        log.error(f"Error retrieving value from Redis: {e}")
        return default_value


def acquire_lock(lock_name):
    lock = redis_client.lock(lock_name)
    acquired = lock.acquire(blocking=False)
    return acquired, lock


def update_stats():
    acquired, lock = acquire_lock('update_stats_lock')
    if acquired:
        try:
            log.info('Updating the statistics for the landing page')

            # The following stats are replicated using the logic from CKAN 2.10
            store_value('ckanext.advancedstats.dataset_count', logic.get_action('package_search')({}, {'rows': 1})['count'])
            store_value('ckanext.advancedstats.group_count', len(logic.get_action('group_list')({}, {})))
            store_value('ckanext.advancedstats.organization_count', len(logic.get_action('organization_list')({}, {})))

            # The following stats are added by ckanext-advancedstats
            q_res = model.Session.query(model.Resource) \
                .join(model.Package) \
                .filter(model.Package.state == 'active') \
                .filter(model.Package.private == False) \
                .filter(model.Resource.state == 'active')

            store_value('ckanext.advancedstats.resource_count', len(q_res.all()))
            store_value('ckanext.advancedstats.jupyter_count', len(q_res.filter(getattr(model.Resource, 'url').ilike('%' + '.ipynb')).all()))

            if sparql is not None:
                triples = 0
                try:
                    res = sparql.queryAndConvert()
                    for r in res['results']['bindings']:
                        triples = r['count']['value']
                except Exception:
                    pass
            else:
                triples = -1
            store_value('ckanext.advancedstats.triples', triples)
            store_value('ckanext.advancedstats.datetime', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        finally:
            import time
            time.sleep(20)  # wait a moment before releasing the lock in order to catch some of the other workers
            lock.release()
            log.debug('Task execution complete, lock released.')
    else:
        log.debug('Task execution skipped, another worker holds the lock.')


class Scheduler:
    instance = None

    class __Scheduler:
        def __init__(self):
            redis_url_parsed = urlparse(redis_url)
            jobstores = {
                'default': RedisJobStore(
                    jobs_key='apscheduler.jobs',
                    run_times_key='apscheduler.run_times',
                    host=redis_url_parsed.hostname,
                    port=redis_url_parsed.port,
                    db=int(redis_url_parsed.path.replace('/', ''))
                )
            }

            scheduler = BackgroundScheduler(jobstores=jobstores, job_defaults={'coalesce': True, 'max_instances': 1}, timezone='UTC')
            scheduler.start()
            try:
                scheduler.add_job(update_stats, 'interval', minutes=interval, next_run_time=datetime.utcnow() + timedelta(minutes=1), id='ckanext.advancedstats:update_stats')
            except ConflictingIdError:
                pass

    def __new__(cls, *args, **kwargs):
        if not Scheduler.instance:
            Scheduler.instance = Scheduler.__Scheduler()
        return Scheduler.instance

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)
