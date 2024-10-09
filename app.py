import json

from flask import Flask, url_for, request, render_template, jsonify
from markupsafe import escape
from Modules.Cat import Cat
from Config.mysqlConfig import db
from Modules.myDatabase import CatModel
from flask_restx import Api, Resource, fields
import pymysql
from flasgger import Swagger, swag_from


app = Flask(__name__)
app.config.from_object('Config.config')
db.init_app(app)
with app.app_context():
    db.create_all() # 在调用create_all()之前，必须导入需要操作的模型，否则不会创建表
swagger = Swagger(app)
# 指定触发函数的URL路径
# 浏览器中访问路径，一定要注意、如果route中没有以反斜杠结尾，访问时就不可以加
# 如果以反斜杠结尾 那访问时加不加都可以
# url_for 构建指定URL


@app.route('/')
def hello_world():  # put application's code here
    with app.test_request_context():
        print(url_for('hello_demo'))  # 跟模板超链接跳转相关
        print(url_for('show_id', id=1))
    return 'Hello World!'

# 具体的URL
@app.route('/hello')
def hello_demo():
    return 'flask'


# URL带参数
@app.route('/hello/<name>')
def hello_name(name):
    print(type(name))
    #return f'hello{name}'
    return f'hello{escape(name)}'  # escape转义  确保嵌入HTML中的字符能够正常转义

# 传入特定类型 int float
'''
int
float
path
string 默认类型
uuid
'''

@app.route('/post/<int:id>')
def show_id(id):
    print(type(id))
    #return f'hello{name}'
    return f'show_id{id}'  # escape转义  确保嵌入HTML中的字符能够正常转义


# 构建指定方法
# @app.route("/request", methods=["POST", 'GET'])
# def request_demo():
#     return 'post请求方法实例'


# @app.get("/request_1")
# def request_demo1():
#     return 'get请求方法实例'


# @app.post("/request_2")
# def request_demo2():
#     return 'post请求方法实例'

# 一个方法两种请求
# @app.route('/cat_add', methods=['GET', 'POST'])
# def cat_add():
#     if request.method == 'GET':
#         return render_template('cat_add.html')
#     else:
#         id = int(request.form['id'])
#         age = request.form['age']
#         name = request.form['name']
#         catlist.append(Cat(id, age, name))
#         return render_template('cat_list.html', catlist=catlist)
@swag_from('./swagger_yaml/cat_add.yaml')
@app.route('/cat_add', methods=['POST'])
def cat_add():
    if not request.content_type == 'application/json':
        return {'code': 400, 'success': False, 'data': '无效的请求方式，请以json形式传递'}
    id = int(request.json['id'])
    age = request.json['age']
    name = request.json['name']
    data = CatModel.query.all()
    for cat in data:
        if cat.id == id:
            return {'code': 400, 'success': False, 'data': '有重复id号'}
    cat = CatModel(id=id, name=name, age=age)
    db.session.add(cat)
    db.session.commit()
    return {'code': 200, 'success': True, 'data': id}

# @app.route('/cat_add', methods=['GET', 'POST'])
# def cat_add():
#     if request.method == 'GET':
#         return render_template('cat_add.html')
#     else:
#         if not request.content_type == 'application/json':
#             return {'code':400, 'success':False, 'data':'无效的请求方式，请以json形式传递'}
#         data = request.get_json()
#         id = data['id']
#         for tmp_cat in catlist:
#             if tmp_cat.id == id:
#                 return {'code': 400, 'success':False, 'data': '有重复id号'}
#         name = data['name']
#         age = data['age']
#         catlist.append(Cat(id, name, age))
#         return {'code': 200, 'success': True, 'data': id}

        # id = int(request.form['id'])
        # age = request.form['age']
        # name = request.form['name']
        # catlist.append(Cat(id, age, name))
        # #return render_template('cat_list.html', catlist=catlist)
        # return {'code': 200, 'success': True, 'data': id}

# 模版 render_template()
# 这是没有变量渲染的模版
@app.route('/template_1')
def template_show():
    return render_template('template1.html')

# 有变量渲染 传入参数
@app.route('/template_2/<name>')
def template_trans_name(name):

    return render_template('template2.html', name=name)

catlist = [
    Cat(1, 'cc', 10),
    Cat(2, 'dd', 20),
    Cat(3, 'ff', 30)
]

# cat_list
# @app.get('/cat_list')
# def cat_list():
#     return render_template('cat_list.html', catlist=catlist)

# @app.get('/cat_list')
# def cat_list():
#     tmp_data = []
#     for cat in catlist:
#         tmp = {}
#         tmp['id'] = cat.id
#         tmp['name'] = cat.name
#         tmp['age'] = cat.age
#         tmp_data.append(tmp)
#     result = {'code': 200, 'success': True, 'data': tmp_data}
#     return jsonify(result)

@app.get('/cat_list')
def cat_list():
    tmp_data = []
    data = CatModel.query.all()
    for cat in data:
        tmp = {}
        tmp['id'] = cat.id
        tmp['name'] = cat.name
        tmp['age'] = cat.age
        tmp_data.append(tmp)
    result = {'code': 200, 'data': tmp_data}
    return jsonify(result)

# @app.get('/cat_detail/<int:id>')
# def cat_detail(id):
#     for cat in catlist:
#         if cat.id == id:
#             return render_template('cat_detail.html', cat=cat)

# @app.get('/cat_detail/<int:id>')
# def cat_detail(id):
#     for cat in catlist:
#         if cat.id == id:
#             tmp_obj = {'id': cat.id, 'name': cat.name, 'age': cat.age}
#             #return render_template('cat_detail.html', cat=cat)
#             return {"code": 200, 'success': True, "data": tmp_obj}


@app.get('/cat_detail/<int:id>')
def cat_detail(id):
    tmp_data = []
    data = CatModel.query.all()
    tmp = {}
    for cat in data:
        if cat.id == id:
            tmp['id'] = cat.id
            tmp['name'] = cat.name
            tmp['age'] = cat.age
            tmp_data.append(tmp)
    result = {'code': 200, 'data': tmp_data, 'success': True}
    return jsonify(result)


"""
json.load() json转化成字典
json.dump() 字典转化成json 格式的字符串
jsonify dict --> json
"""
@app.route('/json/loads')
def json_demo():
    json_demo = '{"id":1,"name":"cc","age":10}'
    result = json.loads(json_demo)
    print(type(result))
    return result

@app.route('/json/dumps')
def dumps_demo():
    json_demo = {"id":1, "name":"cc", "age":10}
    result = json.dumps(json_demo)
    print(type(result))
    return result


@app.route('/json/jsonify')
def jsonify_demo():
    json_demo = {"id":1, "name":"cc", "age":10}
    result = jsonify(json_demo)
    print(type(result))
    return result


if __name__ == '__main__':
    # 终端 flask --app  app run
    # flask --app  app run -p 5001 --debug
    app.run(host='0.0.0.0', port=5000, debug=True)

