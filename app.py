import imp
import os
from flask import Flask, request, jsonify
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello, healthall '

@app.route('/apitest', methods = ['POST'])
def postTest():
    print(request.is_json)
    apiTest = request.get_json()#json 데이터를 받아옴
    print(apiTest['alamst_010'])
    print(apiTest['alamst_020'])
    return (apiTest['alamst_010'] + "," + apiTest['alamst_020'] 
    + "\n" + apiTest['jsonTest']['test1'] + "\n" 
    + apiTest['jsonTest']['test2'])# 받아온 데이터를 다시 전송

'''
@app.route('/stringTest', methods = ['POST'])
def stringTest():
    stringData = request.values
    return stringData
'''
    
 
@app.route('/getmessage/<message>')
def environments(message):
    return jsonify({"message":message})
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0")


