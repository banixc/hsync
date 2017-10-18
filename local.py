#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from file import read_file, Server, diff
import pickle
import sys

operate_section = []

server_list = Server.get_server_list('local.conf')


def request(server_url):
    tree_list = requests.get(server_url).content
    if len(tree_list) == 0:
        return None
    return pickle.loads(tree_list)


def post(server_url, f):
    print 'uploading %s' % f.path
    requests.post(server_url, data=read_file(f))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        operate_section = server_list.keys()
    else:
        operate_section = sys.argv[1:]
    for section in operate_section:
        if section not in server_list:
            print('%s not in local.conf!' % section)
            continue
        else:
            server = server_list[section]
            print('start sync %s : %s' % (section, server.sync_url))
            os.chdir(server.root)
            server_file_list = request(server.get_server_url())
            if server_file_list is None:
                print('server not have %s' % section)
                continue
            local_file = server.get_file_list()

            new, update, old, same = diff(local_file, server_file_list)
            print 'new: %s, update: %s, old: %s, same: %s' % (len(new), len(update), len(old), len(same))
            for i in (update | new):
                post(server.get_server_url(), i)
            for i in old:
                print '[old][%s]\t%s' % (i.get_mod_time(), i.path)

