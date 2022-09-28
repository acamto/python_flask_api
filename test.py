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
    print(apiTest)
    print(type(apiTest))
    keys = [key for key in apiTest]
    print(type(keys))

    for i in keys :
        print(i)

    result = ""

    if "alamst_010" in keys :
        result = result + "alamst_010 : " + apiTest["alamst_010"] + ", "

    if "alamst_020" in keys :
        result = result + "alamst_020 : " + apiTest["alamst_020"] + ", "

    if "alamst_030" in keys :
        result = result + "alamst_030 : " + apiTest["alamst_030"] + ", "

    if "alamst_040" in keys :
        result = result + "alamst_040 : " + apiTest["alamst_040"]

    return result



    
@app.route('/getmessage/<message>')
def environments(message):
    return jsonify({"message":message})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
