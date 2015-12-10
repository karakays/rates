#!/usr/bin/env python

import re, datetime

def parse_date(s):
    ''' Returns a date from given string in ISO format yyyy-mm-dd'''
    if not s:
        raise ValueError()

    pattern = r'^\d{4}-\d{2}-\d{2}$'

    match = re.search(pattern, s)

    if not match:
        raise ValueError('Invalid date: ' + s)

    y, m, d = [int(e) for e in s.split('-')]

    if y < 2000 or (m<1 or m>12) or (d<1 or d>31):
        raise ValueError('Invalid date: ' + s)

    return datetime.date(y, m, d)
