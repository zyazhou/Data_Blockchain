import urllib3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,jsonify, request, make_response
from world_cloud import world_cloud
from datetime import datetime
from scrapy import Lagou
import os ,json
from venv import data_config
from werkzeug.utils import secure_filename
from datetime import timedelta

app = Flask(__name__) #数据库配置
app.config.from_object(data_config)
db=SQLAlchemy(app)
#定义用户表
#定义用户表
class User(db.Model):
    __tablename__ = 'login_user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(50),nullable=False)#用户名
    password=db.Column(db.String(50),nullable=False)#密码
    money= db.Column(db.Integer, autoincrement=True)  # 余额
    phone=db.Column(db.String(11),nullable=True)#电话
    email=db.Column(db.String(30),nullable=False)#邮箱

class Blockchain(db.Model,):
    __tablename__ = 'blockchain'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    index=db.Column(db.Integer,nullable=True)#
    pre_hash=db.Column(db.String(50),nullable=False)#
    message=db.Column(db.String(50),nullable=False)#
    hash=db.Column(db.String(30),nullable=False)#

db.create_all()
app.debug=True

IMG_PATH = "//static/images/scrapy_files/"

@app.route('/',methods=['POST','GET'])
def main():
	return render_template('index.html')

#展示图片的接口
@app.route('/display/img/<filename>', methods=['GET'])
def display_img(filename):
    request_begin_time = datetime.today()
    print("request_begin_time", request_begin_time)
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(IMG_PATH + filename, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            print(response)
            return response
    else:
        pass

@app.route('/showmore',methods=['POST','GET'])
def showmore():
    username = request.values.get('username')
    user = User.query.filter(User.username == username).first()
    data={
        'username':username,
        'money': user.money,
        'email': user.email,
        'phone': user.phone,
    }
    return jsonify(data), 200

@app.route('/user_login',methods=['POST','GET'])
def user_login():
    username = request.values.get('username')
    passwd=request.values.get('passwd')
    print(username)
    print(passwd)

    user = User.query.filter(User.username ==username).first()
    print('00000')
    if(user.password ==passwd):
            data={
                'username':username,
                'passwd':passwd
            }
            print('00001')
            resp = make_response("suess")
            resp.set_cookie("username", username, max_age=3600)
            resp.set_cookie("passwd", passwd, max_age=3600)
            #sendToNodes('127.0.0.1','/set_cookie',data)
            return resp,200
        #print(user.username)
    else:
        response = {
            'result':'no',
            'message': 'fail',
        }
        return jsonify(response),400
@app.route('/show_blockchain',methods=['POST','GET'])
def show_blockchain():
    return render_template('showBlockchain.html')


@app.route('/search_blockchain',methods=['POST','GET'])
def search_blockchain():
    items=[]
    for i  in range (0,4):
        t = Blockchain.query.filter(Blockchain.index == i).first()
        tem={}
        tem['index']=t.index
        tem['hash'] = t.hash
        tem['message'] = t.message
        tem['pre_hash'] = t.pre_hash
        items.append(tem)
        tem={}
    return jsonify(items),200

@app.route('/analysis',methods=['POST','GET'])
def analysis():
	return render_template('Analysis_words.html')


@app.route('/analysis_words/<keyword>',methods=['POST','GET'])
def analysis_words(keyword):
    file_path='./files/scrapy_files/'
    file_path=file_path+keyword+'.txt'

    if (os.path.exists(file_path) == True):
        print(1111)
    else:

        f = open(file_path, 'wb+')
        hot = Lagou(keyword,f)
       # hot = Lagou()
        page_source = hot.search(keyword)
        #hot.get_jobs(page_source)
        #f.write(hot.get_jobs(page_source) + b'\n')
        hot.get_jobs(page_source)
        for i in range(1, 8):
            page_source0 = hot.repeat()
            #hot.get_jobs(page_source0)
            #f.write(hot.get_jobs(page_source0) + b'\n')
            hot.get_jobs(page_source0)
        f.close()
    world_cloud(keyword)

    return '200'

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['txt', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
#实现上传文件接口
@app.route('/uploadfile',methods=['POST,"GET'])
def uploadfile():


        # 通过file标签获取文件
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "图片类型：png、PNG、jpg、JPG、bmp"})
        # 当前文件所在路径
        basepath = os.path.dirname(__file__)
        # 一定要先创建该文件夹，不然会提示没有该路径
        upload_path = os.path.join(basepath, 'static/upload', secure_filename(f.filename))
        # 保存文件
        f.save(upload_path)
        # 返回上传成功界面
        return '200'
    # 重新返回上传界面




#找到响应的文件并进行处理,返回文件名
@app.route('/datasfile_require',methods=['POST','GET'])
def datasfile_require():
    key=request.values.get('username')

    return 0
#节点1的接口
prepare_num=1
commit_num=1

@app.route('/node1/CS',methods=['POST','GET'])
def node1_CS():
    global prepare_num
    global commit_num
    messages = request.get_json().get('messages')
    if(messages=='request'):
        data = {
            'messages': 'prepare_0'
        }
        #sendToNodes('127.0.0.1', '/node1/CS', data)
        sendToNodes('127.0.0.1', '/node2/CS', data)
        sendToNodes('127.0.0.1', '/node3/CS', data)
        sendToNodes('127.0.0.1', '/node4/CS', data)

    if(messages=="prepare_1"): #prepare
        prepare_num=prepare_num+1
        if(prepare_num==3):
            data = {
                messages: 'prepare_1'
            }
            prepare_num=1
            sendToNodes('127.0.0.1', '/node2/CS', data)
            sendToNodes('127.0.0.1', '/node3/CS', data)
            sendToNodes('127.0.0.1', '/node4/CS', data)

    if(messages=="commit_0"): #prepare
        commit_num=commit_num+1
        if(commit_num==3):
            data = {
                messages: 'commit_1'
            }
            commit_num=1
            sendToNodes('127.0.0.1', '/node2/CS', data)
            sendToNodes('127.0.0.1', '/node3/CS', data)
            sendToNodes('127.0.0.1', '/node4/CS', data)
            #交易完成

    if(messages=='commit'):
        data={
            messages:'reply'
        }
    return 'succeed',200

#节点2接口
@app.route('/node2/CS',methods=['POST','GET'])
def node2_CS():
    messages = request.get_json().get('messages')
    if (messages == 'prepare_0'):
        data = {
            'messages': 'prepare_1'
        }
        sendToNodes('127.0.0.1', '/node1/CS', data)
    if (messages == 'prepare_1'):
        data = {
            'messages': 'commit_0'
        }
        sendToNodes('127.0.0.1', '/node1/CS', data)
    return 0

#节点3
@app.route('/node3/CS',methods=['POST','GET'])
def node3_CS():
    messages = request.get_json().get('messages')
    if (messages == 'prepare_0'):
        data = {
            'messages': 'prepare_1'
        }
        sendToNodes('127.0.0.1', '/node1/CS', data)
    if (messages == 'prepare_1'):
        data = {
            'messages': 'commit_0'
        }
        sendToNodes('127.0.0.1', '/node1/CS', data)
    return 0
#节点4
@app.route('/node4/CS',methods=['POST','GET'])
def node4_CS():
    messages = request.get_json().get('messages')
    if (messages == 'prepare_0'):
        data = {
            'messages': 'prepare_1'
        }
        sendToNodes('127.0.0.1', '/node1/CS', data)
    if (messages == 'prepare_1'):
        data = {
            'messages': 'commit_0'
        }
        sendToNodes('127.0.0.1', '/node1/CS', data)
    return 0


#接口，实现逻辑回归的分析，
@app.route('/logistic',methods=['POST',"GET"])
def logistic():
    return  0

@app.route("/get_cookie",methods=['POST',"GET"])
def get_cookie():
    username = request.cookies.get("username")  # 获取名字为Itcast_1对应cookie的值
    passwd = request.cookies.get("passwd")  # 获取名字为Itcast_1对应cookie的值
    data={
        'username':username,
        'passwd':passwd
    }
    return jsonify(data),200


@app.route("/delete_cookie",methods=['POST',"GET"])
def delete_cookie():
    resp = make_response("del success")
    resp.delete_cookie("username")
    resp.delete_cookie("passwd")
    return resp


def sendToNodes(url, loc, data):
    data = json.dumps(data).encode('utf-8')
    http = urllib3.PoolManager()
    res = http.request(
        'POST',
        'http://' + url +':5000' + loc,
        body=data,
        headers={'Content-Type': 'application/json',"Connection":"close"}
    )
    #print('访问了http://' + str(node) + ':5000' + loc)




if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=5000,debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True)