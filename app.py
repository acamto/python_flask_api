import imp
import os
from flask import Flask, request, jsonify
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello, healthall '

@app.route('/apitest', methods = ['POST'])
def userLogin():
    user = request.get_json()#json 데이터를 받아옴
    return jsonify(user)# 받아온 데이터를 다시 전송
 
@app.route('/getmessage/<message>')
def environments(message):
    return jsonify({"message":message})
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0")


