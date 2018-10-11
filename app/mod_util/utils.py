from urllib.parse import urlparse, urljoin
from flask import request, url_for

from app.mod_util.models import Country, State

from sqlalchemy.types import TypeDecorator, CHAR

def parse_l(value):
    degrees, minutes, seconds = value.split(" ")

    degrees = degrees[:-1]
    minutes = minutes[:-1]
    seconds = seconds[:-1]

    multiplier = 1 if float(degrees) > 0 else -1

    return float(degrees) + multiplier*(float(minutes)/60) + multiplier*(float(seconds)/3600)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def parse_multi_form(form):
    data = {}
    for url_k in form:
        v = form[url_k]
        ks = []
        while url_k:
            if '[' in url_k:
                k, r = url_k.split('[', 1)
                ks.append(k)
                if r[0] == ']':
                    ks.append('')
                url_k = r.replace(']', '', 1)
            else:
                ks.append(url_k)
                break
        sub_data = data
        for i, k in enumerate(ks):
            if k.isdigit():
                k = int(k)
            if i+1 < len(ks):
                if not isinstance(sub_data, dict):
                    break
                if k in sub_data:
                    sub_data = sub_data[k]
                else:
                    sub_data[k] = {}
                    sub_data = sub_data[k]
            else:
                if isinstance(sub_data, dict):
                    sub_data[k] = v

    return data

def dd_to_dms(dd, coord):
    is_positive = dd >= 0
    dd = abs(dd)
    minutes, seconds = divmod(dd*3600,60)
    degrees, minutes = divmod(minutes,60)
    degrees = degrees if is_positive else -degrees
    if coord == 'lat':
        direction = 'N' if degrees >= 0 else 'S'
    elif coord == 'lon':
        direction = 'E' if degrees >= 0 else 'W'
    return '{}\xb0 {:0.2f}\' {:0.2f}\'\' {}'.format(degrees,minutes,seconds,direction)
    # return (degrees,minutes,seconds)