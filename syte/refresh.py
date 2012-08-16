#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time

from syte.views import github, bitbucket, ohloh


def refresh(page):
    mapping = {
        'github': (github.github, 'eventh'),
        'bitbucket': (bitbucket.bitbucket, 'eventh'),
        'ohloh': (ohloh.ohloh, 'Eventh'),
    }

    if page not in mapping:
        print 'Invalid page request: %s' % page
        return

    now = time.time()
    func, user = mapping[page]
    response = func(None, user, refresh=True)
    print "Refreshed '%s', status: %i, %.2f seconds" % (
        page, response.status_code, time.time() - now)


if __name__ == '__main__':
    for page in sys.argv[1:]:
        refresh(page)
