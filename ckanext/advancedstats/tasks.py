from datetime import datetime, timedelta
from logging import getLogger
from urllib.parse import urlparse

import ckan.logic as logic
import ckan.model as model
import ckanext.advancedstats.helpers as helpers
from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from ckan.common import config
from ckanext.advancedstats.helpers import acquire_lock, store_value, redis_url, UPDATE_FREQUENCY_KEY

log = getLogger(__name__)


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

            users = model.Session.query(model.User) \
                .filter(model.User.state == 'active') \
                .all()
            store_value('ckanext.advancedstats.user_count', len(users))

            if helpers.sparql is not None:
                triples = 0
                try:
                    res = helpers.sparql.queryAndConvert()
                    for r in res['results']['bindings']:
                        triples = r['count']['value']
                except Exception as e:
                    log.exception(e)
            else:
                triples = -1
            store_value('ckanext.advancedstats.triples', triples)
            store_value('ckanext.advancedstats.datetime', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
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
        job_id = 'ckanext.advancedstats:update_stats'

        def __init__(self):
            redis_url_parsed = urlparse(redis_url)

            self.scheduler = BackgroundScheduler(
                jobstores={
                    'default': RedisJobStore(
                        jobs_key='apscheduler.jobs',
                        run_times_key='apscheduler.run_times',
                        host=redis_url_parsed.hostname,
                        port=redis_url_parsed.port,
                        db=int(redis_url_parsed.path.replace('/', ''))
                    )
                },
                job_defaults={
                    'coalesce': True,
                    'max_instances': 1,
                    'misfire_grace_time': None
                },
                timezone='UTC')

            self.scheduler.start(paused=True)
            try:
                interval = int(config.get(UPDATE_FREQUENCY_KEY))
                self.scheduler.add_job(update_stats, 'interval', minutes=interval, next_run_time=datetime.utcnow() + timedelta(minutes=1), id=self.job_id)
            except ConflictingIdError:
                pass
            self.scheduler.resume()

        def update_interval(self):
            interval = int(config.get(UPDATE_FREQUENCY_KEY))
            self.scheduler.add_job(update_stats, 'date', run_date=datetime.utcnow())
            self.scheduler.reschedule_job(self.job_id, trigger='interval', minutes=interval, start_date=datetime.utcnow())

    def __new__(cls, *args, **kwargs):
        if not Scheduler.instance:
            Scheduler.instance = Scheduler.__Scheduler()
        return Scheduler.instance

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)

    def update_interval(self):
        self.instance.update_interval()
