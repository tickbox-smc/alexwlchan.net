# -*- encoding: utf-8

import pytest

import reports


@pytest.mark.parametrize('log_line', [
    # Unusual methods
    '0.0.0.0 - - [01/Jan/2001:00:00:00 +0000] "HEAD /example HTTP/1.0" 200 0 "http://referrer.org" "Example user agent" "1.2.3.4"',
    '0.0.0.0 - - [01/Jan/2001:00:00:00 +0000] "OPTIONS /example HTTP/1.0" 200 0 "http://referrer.org" "Example user agent" "1.2.3.4"',
    
    # Referrer is empty
    '0.0.0.0 - - [01/Jan/2001:00:00:00 +0000] "GET /example HTTP/1.0" 200 0 "" "Example user agent" "1.2.3.4"',

    # User agent is empty
    '172.18.0.5 - - [22/Dec/2017:03:23:06 +0000] "GET /robots.txt HTTP/1.0" 200 24 "-" "" "198.27.80.144, 108.162.219.92"',
])
def test_nginx_regex(log_line):
    assert reports.NGINX_LOG_REGEX.match(log_line) is not None


log_line_params = {
    'forwarded_host': '1.2.3.4',
    'datetime': '01/Jan/2001:00:00:00 +0000',
    'method': 'GET',
    'url': '/?ref=http://referrer.org',
    'status': '200',
    'bytes_sent': '0',
    'user_agent': 'WebKit',
}


@pytest.mark.parametrize('override_params, expected_result', [
    ({'url': '/?ref=http://yandex.ru'}, True),
])
def test_should_be_rejected(override_params, expected_result):
    params = log_line_params.copy()
    params.update(override_params)
    line = reports.LogLine(**params)
    assert reports.should_be_rejected(line) is expected_result
