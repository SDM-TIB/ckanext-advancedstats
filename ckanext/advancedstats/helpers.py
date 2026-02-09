import os
import socket
from logging import getLogger
from urllib.error import URLError, HTTPError

import ckan.plugins.toolkit as toolkit
import redis
from SPARQLWrapper import SPARQLWrapper, JSON
from ckan.common import config

log = getLogger(__name__)
redis_url = os.getenv('CKAN_REDIS_URL', 'redis://localhost:6379/0')
redis_client = redis.from_url(redis_url)
sparql = None

SELECTED_STATS_KEY = 'ckanext.advancedstats.stats'
UPDATE_FREQUENCY_KEY = 'ckanext.advancedstats.updatefrequency'
KG_URL_KEY = 'ckanext.advancedstats.kg'


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
    lock = redis_client.lock(lock_name, timeout=30)
    acquired = lock.acquire(blocking=False)
    return acquired, lock


def endpoint_accessible(url):
    sparql = SPARQLWrapper(url)
    sparql.setTimeout(5)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("ASK { ?s ?p ?o }")  # cheap sanity query (may still be denied by some endpoints)

    try:
        r = sparql.query().convert()
        return bool(r.get("boolean", True))
    except (HTTPError, URLError, socket.timeout, Exception):
        return False


def init_sparql():
    global sparql
    kg_url = config.get(KG_URL_KEY, None)
    if kg_url is None:
        sparql = None
    else:
        sparql = SPARQLWrapper(kg_url)
        sparql.setReturnFormat(JSON)
        sparql.setQuery('SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }')


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


init_sparql()
