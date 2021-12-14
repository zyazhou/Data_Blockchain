from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import data_config
app = Flask(__name__)
app.config.from_object(data_config)
db=SQLAlchemy(app)

import hashlib #hash加密
md5 = hashlib.md5()  # 应用MD5算法
#data = "hello world"
#md5.update(data.encode('utf-8'))
#print(md5.hexdigest())

#定义用户表
class User(db.Model):
    __tablename__ = 'login_user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(50),nullable=False)#用户名
    password=db.Column(db.String(50),nullable=False)#密码
    phone=db.Column(db.String(11),nullable=True)#电话
    email=db.Column(db.String(30),nullable=False)#邮箱

class nodes(db.Model):
    __tablename__ = 'nodes'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)

    N_id=db.Column(db.Integer,nullable=True)#
    public_name=db.Column(db.String(50),nullable=False)#
    private_name=db.Column(db.String(50),nullable=False)#
    N_ip=db.Column(db.String(30),nullable=False)#ip
    N_suc = db.Column(db.Integer, nullable=False)  #
    N_fail = db.Column(db.Integer, nullable=False)  #

class Blockchain(db.Model,):
    __tablename__ = 'blockchain'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    index=db.Column(db.Integer,nullable=True)#
    pre_hash=db.Column(db.String(1000),nullable=False)#
    message=db.Column(db.String(1000),nullable=False)#
    hash=db.Column(db.String(1000),nullable=False)#ip



# #定义用户信息表
# class  user_OP(db.Model):
#     __tablename__='login_user_OP'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     OP_id=db.Column(db.Integer,nullable=False)#操作记录
#     OP_type=db.Column(db.String(50),nullable=False)#
#     OP_time=db.Column(db.DateTime,default=datetime.now)#时间
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     users = db.relationship('User', backref=db.backref('cards'), uselist=False)
db.create_all()
@app.route('/add')
def add():
    #添加两条用户数据
    user1 = User(username="zya", password="123456", phone="18079690671", email="2534719204@qq.com")
    db.session.add(user1)
    db.session.commit()
    return '添加数据成功！'

@app.route('/nodes_register')
def register():
    node1=nodes(N_id=1,public_name="node1_public_key", private_name="",N_ip="", N_suc="881",N_fail="4")
    node2=nodes(N_id=2, public_name="node2_public_key", private_name="", N_ip="", N_suc="882",N_fail="3")
    node3 = nodes(N_id=3, public_name="node3_public_key", private_name="", N_ip="", N_suc="883",
                  N_fail="2")
    node4 = nodes(N_id=4, public_name="node4_public_key", private_name="", N_ip="", N_suc="884",
                  N_fail="1")

    db.session.add(node1)
    db.session.add(node2)
    db.session.add(node3)
    db.session.add(node4)
    db.session.commit()
    return 'succeed!'

@app.route('/Blockchain_updata')
def blockchain_updata():
    data = "The Genesis Block"
    hash=hashlib.sha256(data.encode()).hexdigest()
    print(hash)
    pre_hash='0'
    b1=Blockchain(index=0,pre_hash='0',message='创世纪块',hash=hash)

    pre_hash=hash
    message='000'
    data=message+str(pre_hash)
    hash=hashlib.sha256(data.encode()).hexdigest()
    print(hash)
    b2=Blockchain(index=1,pre_hash=pre_hash,message=message,hash=hash)

    pre_hash=hash
    message='001'
    data=message+str(pre_hash)
    hash=hashlib.sha256(data.encode()).hexdigest()
    b3=Blockchain(index=2,pre_hash=pre_hash,message=message,hash=hash)

    pre_hash=hash
    message='002'
    data=message+str(pre_hash)
    hash=hashlib.sha256(data.encode()).hexdigest()
    b4=Blockchain(index=3,pre_hash=pre_hash,message=message,hash=hash)

    pre_hash=hash
    message='003'
    data=message+str(pre_hash)
    hash=hashlib.sha256(data.encode()).hexdigest()
    b5=Blockchain(index=4,pre_hash=pre_hash,message=message,hash=hash)
    db.session.add(b1)
    db.session.add(b2)
    db.session.add(b3)
    db.session.add(b4)
    db.session.add(b5)
    db.session.commit()
    return "succeed"

@app.route('/select')
def select():
    try:
        user = User.query.filter(User.username == 'zya').first()


        print(user.username)

        return "查询数据成功！"

    except Exception as e:
        return "异常说明！"


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='127.0.0.2',debug=True)
