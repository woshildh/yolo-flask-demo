import os,sys,cgi,shutil,time
import test
import flask
import tensorflow as tf
import cv2
import numpy as np
from yolo.yolo_net import YOLONet
import yolo.config as cfg
from flask_cors import *
from flask import Flask, request,make_response,jsonify,send_file

#设置测试的各项参数
weight_file="./data/weights/YOLO_small.ckpt"
#先加载模型
yolo=YOLONet(is_training=False)

#判断权重文件是否存在,加载权重文件
if os.path.exists(weight_file):
	detector=test.Detector(yolo,weight_file)
else:
	raise ValueError("weight _file not exists")

#定义服务ip和端口号
SERVER_HOST="localhost"
SERVER_PORT=5000
app = Flask(__name__)

#设置支持异步访问
CORS(app, supports_credentials=True)

#用来计数已经上传的图片的数量
count=0

@app.route("/")
def main():
	'''
	访问根目录，返回主页面
	'''
	return send_file("./static/index.html")

def delete_imgs():
	'''
	删除原来上传的图片和新产生的图片
	'''
	img_list1=os.listdir("/".join([os.getcwd(),"test/original/"]))
	img_list2=os.listdir("/".join([os.getcwd(),"test/generated/"]))
	for img in img_list1:
		img_path="/".join([os.getcwd(),"test/original/",img])
		os.remove(img_path)
	for img in img_list2:
		img_path="/".join([os.getcwd(),"test/generated/",img])
		os.remove(img_path)

@app.route('/convert', methods=['GET', 'POST'])
def convert_image():
	'''
	转换图片
	'''
	if request.method == 'POST':
		global count
		image_storage=request.files['files'].read()
		
		original_img_name="./test/original/previous"+str(count)+".jpg"
		with open(original_img_name,'wb') as file:
			file.write(image_storage)
		#成功上传之后,count自增
	
		generated_img_name="./test/generated/"+str(time.time()).split(".")[0]+".jpg"
		detector.image_detector(original_img_name,generated_img_name)
		count+=1
		print("成功转换一张图片...")
		res=make_response(jsonify("true"))
		res.headers['Access-Control-Allow-Origin'] = "*"
		return  res

@app.route("/clear",methods=['POST','GET'])
def clear_image():
	'''
	清除test/generated  和 test/original下的所有的图片
	'''
	if request.method=="POST":
		global count
		command=request.values.get("command")
		print(command)
		if command=="clear":
			delete_imgs()
			count=0
		res=make_response(jsonify("true"))
		res.headers['Access-Control-Allow-Origin'] = "*"
		return  res

@app.route("/get_img",methods=['POST','GET'])
def get_images():
	'''
	获取 test/generated 下的所有的图片列表
	'''
	if request.method=="POST":
		global count
		command=request.values.get("command")
		print(command)
		if command=="get_img":
			#返回的图片名字列表使用;连接
			img_list=";".join(os.listdir("./test/generated/"))
		res=make_response(jsonify(img_list))
		res.headers['Access-Control-Allow-Origin'] = "*"
		return  res

@app.route("/<file_name>")
def style(file_name):
	return send_file("./static/"+file_name)

@app.route("/js/<file_name>")
def get_js(file_name):
	return send_file("./static/js/"+file_name)

@app.route("/img/<file_name>")
def get_img(file_name):
	return send_file("./static/img/"+file_name)

@app.route("/test/generated/<file_name>")
def send_image(file_name):
	'''
	根据超链接请求图片时，把图片返回
	'''
	#res=make_response(send_file("./test/generated/"+file_name))
	#res.headers['Access-Control-Allow-Origin'] = "*"
	return send_file("./test/generated/"+file_name)

if __name__=="__main__":
	app.run(host=SERVER_HOST,port=SERVER_PORT,debug=True)
