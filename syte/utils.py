#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pprint import pprint
from xml.etree import ElementTree

import requests
from django.conf import settings


def list_ohloh_contribution_ids(user, *project_names):
    """List ohloh.net contribution_id for given 'projects'."""
    # Find account_id to match against project contributions
    r = requests.get('{0}accounts/{1}.xml?api_key={2}'.format(
        settings.OHLOH_API_URL, user, settings.OHLOH_API_KEY))

    root = ElementTree.fromstring(r.text)
    error = root.find('error')
    if error is not None:
        print "Fatal error: ", error.text
        sys.exit(1)

    account_id = root.find('result/account/id').text

    # Find id of projects managed by user
    man_r = requests.get('{0}accounts/{1}/projects.xml?api_key={2}'.format(
        settings.OHLOH_API_URL, user, settings.OHLOH_API_KEY))
    root = ElementTree.fromstring(man_r.text)
    projects = [(n.find('url_name').text, n.find('id').text) for
                    n in root.find('result')]

    # Find id of projects listed in 'project_names'
    for name in project_names:
        pro_r = requests.get('{0}p/{1}.xml?api_key={2}'.format(
            settings.OHLOH_API_URL, name, settings.OHLOH_API_KEY))
        root = ElementTree.fromstring(pro_r.text)
        projects.append((name, root.find('result/project/id').text))

    results = []
    for name, project_id in projects:
        found = []

        # Find contributor_id tied to our account_id
        page = 0
        last_page = False
        while not last_page:
            page += 1
            pro_r = requests.get(
                '{0}p/{1}/contributors.xml?api_key={2}&page={3}'.format(
                    settings.OHLOH_API_URL, project_id,
                    settings.OHLOH_API_KEY, page))
            root = ElementTree.fromstring(pro_r.text)

            if (int(root.find('first_item_position').text) +
                int(root.find('items_returned').text) >=
                int(root.find('items_available').text)):
                last_page = True

            for node in root.find('result'):
                values = {n.tag: n.text for n in node}
                if values.get('account_id', None) == account_id:
                    found.append((int(project_id),
                                  int(values['contributor_id'])))

        results.extend(found)
        if not found:
            print "No contributions matching %s (%s) found for %s (%s)" % (
                user, account_id, name, project_id)
        else:
            print "Found for %s:" % name, found

    return results


def main(action='ohloh', *args):
    # Usage: python utils.py ohloh <username> <list of project names>
    if action == 'ohloh':
        pprint(tuple(list_ohloh_contribution_ids(args[0], *args[1:])))
    else:
        print "Invalid usage"
        sys.exit(2)


if __name__ == '__main__':
    main(*sys.argv[1:])
