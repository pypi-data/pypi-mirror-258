# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from my_sdk.database import DatabaseConnector
from difflib import SequenceMatcher
import nltk
from nltk.stem import PorterStemmer

app = Flask(__name__)


# 示例路由，处理 GET 请求
@app.route('/api/resource', methods=['GET'])
def get_resource():
    # 从请求中获取参数
    resource_id = request.args.get('id')

    # 查询资源，这里只是个示例，实际情况可能是从数据库或其他地方获取数据
    resource = {
        'id': resource_id,
        'name': 'Example Resource',
        'description': 'This is an example resource.'
    }

    # 返回 JSON 格式的响应
    return jsonify(resource)


# 示例路由，处理 POST 请求
@app.route('/api/resource', methods=['POST'])
def create_resource():
    # 从请求中获取 JSON 数据
    data = request.json

    # 在数据库中创建资源，这里只是个示例
    # ...

    # 返回成功消息
    return jsonify({'message': 'Resource created successfully.'}), 201


if __name__ == '__main__':
    app.run(debug=True)
