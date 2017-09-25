# coding=utf-8
import os
import requests
from file import read_file, get_file_list, diff, get_config
import pickle

root_path = get_config('local', 'sync_path')
server_url = get_config('local', 'sync_url')


def request():
    tree_list = requests.get(server_url).content
    return pickle.loads(tree_list)


def post(f):
    print 'uploading %s' % f.path
    requests.post(server_url, data=read_file(f))


if __name__ == '__main__':
    os.chdir(root_path)

    server_root = request()
    local_root = get_file_list(root_path)
    new, update, old, same = diff(local_root, server_root)
    print 'new: %s, update: %s, old: %s, same: %s' % (len(new), len(update), len(old), len(same))
    for i in (update | new):
        post(i)
    for i in old:
        print '[old] %s' % i.path
        # post(i)

