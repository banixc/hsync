# coding=utf-8
import pickle
import os
import hashlib
import ConfigParser


def get_config(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/sync.conf'
    config.read(path)
    return config.get(section, key)


exclude_ext = get_config('public', 'exclude_ext').split(';')
sep = '/'


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

    def __eq__(self, other):
        return self.path == other.path and self.md5 == other.md5 and self.mod_time == other.mod_time and self.access_time == other.access_time

    def __hash__(self):
        return hash(self.path) ^ hash(self.md5) ^ hash(self.mod_time) ^ hash(self.access_time)


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
            #if t.mod_time == s.mod_time:
                same.add(s)
            elif t.mod_time > s.mod_time:
                old.add(s)
            elif t.mod_time < s.mod_time:
                overwrite.add(s)
            else:
                print 'err'
    return new, overwrite, old, same


def get_file_list(root_path):
    os.chdir(root_path)
    file_set = set()
    for root, dirs, files in os.walk('.', topdown=False):
        for name in files:
            if os.path.splitext(name)[1] in exclude_ext:
                continue
            file_set.add(File(sep.join((root, name))))
    return file_set


def read_file(f):
    fp = open(f.path, 'rb')
    f.file_data = fp.read()
    return pickle.dumps(f)


def write_file(f):
    f = pickle.loads(f)
    p_path = os.path.split(f.path)[0]
    if p_path != '' and not os.path.exists(p_path):
        os.makedirs(p_path)
    fp = open(f.path, 'wb+')
    fp.write(f.file_data)
    os.utime(f.path, (f.access_time, f.mod_time))


def md5file(path):
    fp = open(path, 'rb')
    return hashlib.md5(fp.read()).hexdigest()


if __name__ == '__main__':
    print repr(exclude_ext)