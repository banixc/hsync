# coding=utf-8
import os
from file import write_file, get_file_list, get_config
from flask import Flask, request
import pickle

app = Flask(__name__)
root_path = get_config('server', 'sync_path') + '/sync'


@app.route('/sync', methods=['GET'])
def get():
    root_tree = get_file_list(root_path)
    return pickle.dumps(root_tree)


@app.route('/sync', methods=['POST'])
def post():
    file_data = request.get_data()
    write_file(file_data)
    return 'success!'


if __name__ == '__main__':
    os.chdir(root_path)
    app.run(debug=True, port=7179)

