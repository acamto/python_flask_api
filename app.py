import imp
import json
import os
import base64
from flask import Flask, request, jsonify
app = Flask(__name__)

alamst_010_hour = None
alamst_010_minute = None

alamst_020_hour = None
alamst_020_minute = None

alamst_030_hour = None
alamst_030_minute = None

alamst_040_hour = None
alamst_040_minute = None
 
@app.route('/')
def hello_world():
    return 'Hello, healthall '


@app.route('/setAlarmTime', methods=['POST'])
def setAlarmTime() :
    print(request.is_json)

    alarmTimeJson = request.get_json

    alarmKey = alarmTimeJson
    #[key for key in alarmTimeJson]

    requestCheckKey = ["morning", "noon", "evening", "night"]

    print (alarmTimeJson)

    alarmDict = None

    checkResult = True
    returnAlarmResult = "success setAlarm"

    for i in alarmKey :
        if i not in requestCheckKey :
            checkResult = False
            returnAlarmResult = "there is wrong alarm"

    if checkResult :

        for i in alarmKey :
            if i in requestCheckKey :
                alarmDict[i + "hour"] = int(alarmTimeJson[i].split(":")[0])
                alarmDict[i + "minute"] = int(alarmTimeJson[i].split(":")[1])
                print(i + "hour : " + int(alarmTimeJson[i].split(":")[0]) 
                + "--> Type : " + type(int(alarmTimeJson[i].split(":")[0])) + "\n" 
                + i + "minute : " + int(alarmTimeJson[i].split(":")[1]) 
                + "--> Type : " + type(int(alarmTimeJson[i].split(":")[1])))
        
        for key in alarmDict:
            print("key: {}, value: {}".format(key, alarmDict[key]))
    else :
        print("worng request")
    
    return returnAlarmResult




@app.route('/getmessage/<message>')
def environments(message):
    return jsonify({"message":message})

@app.route('/setCommand', methods=['POST'])
def commandCabinet() :
    print("put cabinet command")

    commandSet = request.get_json
    keys = [key for key in commandSet]

    for i in keys :
        print(i)

    return "set success"
    
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0")


