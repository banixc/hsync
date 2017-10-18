#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from file import write_file, Server
from flask import Flask, request, make_response, jsonify
import pickle

app = Flask(__name__)
server_list = Server.get_server_list('server.conf')


@app.route('/', methods=['GET'])
def index():
    return jsonify(server_list.keys())


@app.route('/<string:name>', methods=['GET'])
def get(name):
    if name in server_list:
        server = server_list[name]
        os.chdir(server.root)
        root_tree = server.get_file_list()
        return pickle.dumps(root_tree)
    return ''


@app.route('/<string:name>', methods=['POST'])
def post(name):
    if name in server_list:
        server = server_list[name]
        os.chdir(server.root)
        file_data = request.get_data()
        write_file(file_data)
        return 'success!'
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=7179)
