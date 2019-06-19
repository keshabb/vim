import re
import time
from collections import namedtuple
from datetime import datetime


class LogDetails(namedtuple('LogDetails', 'client_ip, user, timestamp, http_method, url, http_protocol, status_code, domain')):
    def to_tags(self, **kwargs):
        tags = self._asdict()
        del tags['timestamp']
        del tags['url']
        tags.update(kwargs)
        return tags


WILDCARD = '*'


class LogRequests(object):
    def __init__(self, logger, line):
        self.details = _get_log_details(logger, line)
        if not self.details:
            return None
        self.url_group = _get_url_group(self.details.url)

def parse_request_total(logger, line):
    log_req = LogRequests(logger, line)
    return 'artifactory.requests.total', log_req.details.timestamp, 1, log_req.details.to_tags(metric_type='counter', url_group=log_req.url_group)


def parse_status_code(logger, line):
    log_req = LogRequests(logger, line)
    if log_req.details[6].startswith('20'):
        return 'artifactory.requests.2xx', log_req.details.timestamp, 1, log_req.details.to_tags(metric_type='counter', url_group=log_req.url_group)
    elif log_req.details[6].startswith('40'):
        return 'artifactory.requests.4xx', log_req.details.timestamp, 1, log_req.details.to_tags(metric_type='counter', url_group=log_req.url_group)
    elif log_req.details[6].startswith('50'):
        return 'artifactory.requests.5xx', log_req.details.timestamp, 1, log_req.details.to_tags(metric_type='counter', url_group=log_req.url_group)

def parse_http_method(logger, line):
    log_req = LogRequests(logger, line)
    if log_req.details[3] == 'GET':
        return 'artifactory.requests.get', log_req.details.timestamp, 1, log_req.details.to_tags(metric_type='counter', url_group=log_req.url_group)
    elif log_req.details[3] == 'PUT':
        return 'artifactory.requests.put', log_req.details.timestamp, 1, log_req.details.to_tags(metric_type='counter', url_group=log_req.url_group)
    elif log_req.details[3] == 'POST':
        return 'artifactory.requests.post', log_req.details.timestamp, 1, log_req.details.to_tags(metric_type='counter', url_group=log_req.url_group)
    elif log_req.details[3] == 'DELETE':
        return 'artifactory.requests.delete', log_req.details.timestamp, 1, log_req.details.to_tags(metric_type='counter', url_group=log_req.url_group)


def parse_api_call(logger, line):
    log_req = LogRequests(logger, line)
    if log_req.details[4].startswith(r'/api') and log_req.details[3] == 'GET':
        return 'artifactory.requests.api.get', log_req.details.timestamp, 1, log_req.details.to_tags(metric_type='counter', url_group=log_req.url_group)
    elif log_req.details[4].startswith(r'/api') and log_req.details[3] == 'PUT':
        return 'artifactory.requests.api.put', log_req.details.timestamp, 1, log_req.details.to_tags(metric_type='counter', url_group=log_req.url_group)
    elif log_req.details[4].startswith(r'/api') and log_req.details[3] == 'POST':
        return 'artifactory.requests.api.post', log_req.details.timestamp, 1,log_req. details.to_tags(metric_type='counter', url_group=log_req.url_group)
    elif log_req.details[4].startswith(r'/api') and log_req.details[3] == 'DELETE':
        return 'artifactory.requests.api.delete', log_req.details.timestamp, 1,log_req. details.to_tags(metric_type='counter', url_group=log_req.url_group)



def _get_log_details(logger, line):
    if not line:
        return None

    try:
        details = _parse_line(line)
    except Exception:
        logger.exception('Failed to parse log line')
        return None

    if _should_skip_log(details.url):
        return None

    return details


def _get_url_group(url):
    default = 'other'
    if url.startswith('/a/' + WILDCARD):
        parts = url.split('/')
        return parts[3] if len(parts) >= 4 else default

    return default


def _should_skip_log(url):
    return re.search(r'^/static/', url)


def _parse_line(line):
    match = re.match(r'(?P<date>[0-9]+)', line)
    string_date = match.group('date')
    date = datetime.strptime(string_date, "%Y%m%d%H%M%S")

    # First two dummy args are from the date being split
    parts = line.split('|')
    client_ip, user, http_method, url, http_protocol, status_code = parts[3], parts[4], parts[5], parts[6], parts[7], parts[8]

    timestamp = time.mktime(date.timetuple())
    domain = _extract_domain(url)
    url = _sanitize_url(url)
    return LogDetails(client_ip, user, timestamp, http_method, url, http_protocol, status_code, domain)


def _sanitize_url(url):
    url = re.sub(r'/a/[0-9a-z-]+', '/a/{}'.format(WILDCARD), url)

    # Remove URL params
    url = re.sub(r'\?[^ ]*', '', url)
    return url


def _extract_domain(url):
    match = re.search(r'/a/(?P<domain>[0-9a-z-]+)', url)
    if not match:
        return ''
    return match.group('domain')
