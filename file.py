#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import hashlib
import ConfigParser
import time
import re
import json
import struct


class Server:
    conf = None
    server_name_list = []

    def __init__(self, name):
        self.name = name
        self.root = self.get_conf('path')
        self.exclude_ext_list = self.get_conf('exclude_ext', '').split(';')
        self.exclude_dir_list = self.get_conf('exclude_dir', '').split(';')
        self.sync_url = self.get_conf('server_url')
        if self.conf.has_option(self.name, 'overwrite'):
            self.overwrite = self.conf.getboolean(self.name, 'overwrite')

    def get_conf(self, key, value=None):
        if Server.conf.has_option(self.name, key):
            return Server.conf.get(self.name, key)
        return value

    def get_file_list(self):
        os.chdir(self.root)
        file_set = set()
        for root, dirs, files in os.walk('.', topdown=False):
            if self.root_exclude(root):
                continue
            for name in files:
                if os.path.splitext(name)[1] in self.exclude_ext_list:
                    continue
                file_set.add(File(sep.join((root, name))))
        return file_set

    def root_exclude(self, root):
        for exclude_dir in self.exclude_dir_list:
            exclude_dir = dir_to_list(exclude_dir)
            root_dir_list = dir_to_list(root)
            if dir_in(root_dir_list, exclude_dir):
                return True
        return False

    def get_server_url(self):
        return self.sync_url

    @classmethod
    def get_server_list(cls, name):
        Server.conf = get_config(name)
        Server.server_name_list = Server.conf.sections()
        return {server_name: Server(server_name) for server_name in Server.server_name_list}


def get_config(name):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/' + name
    config.read(path)
    return config


sep = '/'


def dir_to_list(dir_str):
    dir_list = re.split(r'/|\\', dir_str)
    if '.' in dir_list:
        dir_list.remove('.')
    return dir_list


# 判断dir1是否为dir2的子目录
def dir_in(dir1, dir2):
    if len(dir1) < len(dir2):
        return False
    for i in range(len(dir2)):
        if dir1[i] != dir2[i]:
            return False
    return True


class File:
    def __init__(self, path, md5=None, access_time=None, mod_time=None, file_data=None):
        if type(path) == unicode:
            path = path.encode('utf-8')
        if type(md5) == unicode:
            md5 = md5.encode('utf-8')
        self.path = sep.join(path.split(os.sep))
        self.md5 = md5file(path) if md5 is None else md5
        self.access_time = int(os.path.getctime(self.path)) if access_time is None else access_time
        self.mod_time = int(os.path.getmtime(self.path)) if mod_time is None else mod_time
        self.file_data = None if file_data is None else file_data

    def get_mod_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.mod_time))

    def __eq__(self, other):
        return self.path == other.path and self.md5 == other.md5 and self.mod_time == other.mod_time and self.access_time == other.access_time

    def __hash__(self):
        return hash(self.path) ^ hash(self.md5) ^ hash(self.mod_time) ^ hash(self.access_time)

    def to_json(self):
        return json.dumps({
            'path': self.path,
            'md5': self.md5,
            'access_time': self.access_time,
            'mod_time': self.mod_time,
            'file_data': self.file_data
        })

    def read_file(self):
        data = open(self.path, 'rb').read()
        self.file_data = struct.unpack('%sB' % len(data), data)

    def write_file(self):
        p_path = os.path.split(self.path)[0]
        if p_path != '' and not os.path.exists(p_path):
            os.makedirs(p_path)
        data = struct.pack('%sB' % len(self.file_data), *self.file_data)
        fp = open(self.path, 'wb+')
        fp.write(data)
        os.utime(self.path, (self.access_time, self.mod_time))

    @staticmethod
    def from_json(json_data):
        data_dict = json.loads(json_data)
        return File(path=data_dict['path'], md5=data_dict['md5'], access_time=data_dict['access_time'],
                    mod_time=data_dict['mod_time'], file_data=data_dict['file_data'])


def diff(source, targets):
    target_dic = {}
    for target in targets:
        target_dic[target.path] = target
    new = set()
    overwrite = set()
    old = set()
    same = set()
    for s in source:
        t = target_dic.get(s.path, None)
        if t is None:
            new.add(s)
        else:
            if t.md5 == s.md5:
                same.add(s)
            elif t.mod_time > s.mod_time:
                old.add(s)
            elif t.mod_time < s.mod_time:
                overwrite.add(s)
            else:
                print 'err'
    return new, overwrite, old, same


def md5file(file_path):
    fp = open(file_path, 'rb')
    return hashlib.md5(fp.read()).hexdigest()

