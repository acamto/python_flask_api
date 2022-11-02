import base64
import json
import os
import time
from flask import Flask, request, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)

global alarmDict 
alarmDict = {"0x7C" : {}, "0x7B" : {}, "0x7F" : {}, "0x7E" : {}, "0x6B" : {}, "0x6C" : {}}

global stateDict 
stateDict ={}

global checkNum
checkNum = 0

app.config['MQTT_BROKER_URL'] = '192.168.0.25'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  
app.config['MQTT_PASSWORD'] = '' 
app.config['MQTT_KEEPALIVE'] = 5  
app.config['MQTT_TLS_ENABLED'] = False  
topic = '/flask/mqtt'

mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(topic) # subscribe topic
    else:
        print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global checkNum
    checkNum += 1
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))
    print('message check : ' + str(checkNum))


@app.route('/publish', methods=['POST'])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return jsonify({'code': publish_result[0]})




'''
@app.route('/')
def hello_world():
    return 'Hello, healthall '


@app.route('/setCabinetSetting', methods = ['POST'])
def setTime():

    checkResult = True
    returnAlarmResult = "success setCabinetSetting"
    global alarmDict 
    
    
    print(request.is_json)

    cabinetSettingJson = request.get_json()
    print(type(cabinetSettingJson))
    #print(cabinetSettingJson)
    

    alarmAlarmKey = [key for key in cabinetSettingJson["0x7C"]]
    alarmActiveKey = [key for key in cabinetSettingJson["0x7B"]]
    alarmStateKey = [key for key in cabinetSettingJson["0x7F"]]
    #alarmNowTimeKey = [key for key in cabinetSettingJson["0x7E"]]
    alarmLEDKey = [key for key in cabinetSettingJson["0x6B"]]
    alarmStartKey = [key for key in cabinetSettingJson["0x6C"]]

    requestAlarmCheckKey = ["morningTime", "noonTime", "eveningTime", "nightTime"]
    requestActiveCheckKey = ["morningActive", "noonActive", "eveningActive", "nightActive"]
    requestStateCheckKey = ["morningState", "noonState", "eveningState", "nightState"]
    #requestNowTimeCheckKey = ["nowHour", "nowMinute", "nowSecond"]
    requestLEDCheckKey = ["firstLEDState", "secondLEDState", "thirdLEDState", "fourthLEDState", "fifthLEDState", "sixthLEDState", "seventhLEDState"]
    requestStartCheckKey = ["alarmStart"]
    

    for i in alarmAlarmKey :
        if i not in requestAlarmCheckKey :
            checkResult = False
            returnAlarmResult = "there is wrong setting"

    for i in alarmActiveKey :
        if i not in requestActiveCheckKey :
            checkResult = False
            returnAlarmResult = "there is wrong setting"

    for i in alarmStateKey :
        if i not in requestStateCheckKey :
            checkResult = False
            returnAlarmResult = "there is wrong setting"

    
    for i in alarmLEDKey :
        if i not in requestLEDCheckKey :
            checkResult = False
            returnAlarmResult = "there is wrong setting"
    

    if checkResult :
        for i in alarmAlarmKey :
            if i in requestAlarmCheckKey :                
                alarmDict["0x7C"][i + "_hour"] = int(cabinetSettingJson["0x7C"][i].split(":")[0])
                alarmDict["0x7C"][i + "_minute"] = int(cabinetSettingJson["0x7C"][i].split(":")[1])

        for i in alarmActiveKey :
            if i in requestActiveCheckKey :                
                alarmDict["0x7B"][i] = int(cabinetSettingJson["0x7B"][i])

        for i in alarmStateKey :
            if i in requestStateCheckKey :                
                alarmDict["0x7F"][i] = int(cabinetSettingJson["0x7F"][i])

        alarmDict["0x7E"]["nowHour"] = int(time.strftime('%H'))
        alarmDict["0x7E"]["nowMinute"] = int(time.strftime('%M'))
        alarmDict["0x7E"]["nowSecond"] = int(time.strftime('%S'))
        
        for i in alarmLEDKey :
            if i in requestLEDCheckKey :                
                alarmDict["0x6B"][i] = int(cabinetSettingJson["0x6B"][i])

        for i in alarmStartKey :
            if i in requestStartCheckKey :
                alarmDict["0x6C"][i] = int(cabinetSettingJson["0x6C"][i])
       
                                
        for key in alarmDict:
            for keys in alarmDict[key]:
                print("key: {}, value: {}, type :{}".format(keys, alarmDict[key][keys], type(alarmDict[key][keys])))
    else :
        print("worng request")
    
    return returnAlarmResult


@app.route('/getmessage/<message>')
def environments(message):
    return jsonify({"message":message})


@app.route('/setCommand', methods=['POST'])
def commandCabinet() :
    print("put cabinet command")
    global alarmDict
    
    commandSet = request.get_json()
    keys = [key for key in commandSet]

    for i in keys :
        print(i)
        print(commandSet[i])

    if commandSet["value"] == "setCommand" :
        print(json.dumps(alarmDict, ensure_ascii=False))
        return json.dumps(alarmDict, ensure_ascii=False)

@app.route('/setState', methods=['POST'])
def stateCabinet() :
    print("set Cabinet Status")
    requestSetCheckKey = ['TAG', 'dosing number', 'alarm hour', 'alarm minutes',
    'activation value', 'Whether to take', 'take hour', 'take minutes',
    'operation hour', 'operation minutes', 'AND or END']
    checkResult = True
    returnSetResult = "success setStatus"
    global stateDict 
    print(request.is_json)
    cabinetState = request.get_json()
    print(type(cabinetState))
    print(cabinetState)
    
    setKey = [key for key in cabinetState]

    for i in setKey :
        if i not in requestSetCheckKey :
            checkResult = False
            returnSetResult = "there is wrong alarm"

    if checkResult :

        for i in setKey :
            if i in requestSetCheckKey :
                stateDict[i] = int(cabinetState[i])
        
        for key in stateDict:
            print("key: {}, value: {}, type :{}".format(key, stateDict[key], type(stateDict[key])))
    else :
        print("worng request")

    return returnSetResult

@app.route('/setTakeState', methods=['POST'])
def setTakeState() :
    print("set Cabinet take Status")
    requestSetStateKey = ['TAG', 'dosing number', 'alarm hour', 'alarm minutes', 'taking hour', 'taking minutes']
    print(request.is_json)
    pillTakeState = request.get_json()
    print(pillTakeState)
    return 1

    

@app.route('/testMessage', methods=['POST'])
def testMessage() :
    print(request.is_json)
    testMessage = request.get_json()
    print(testMessage)
    return "test success"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
'''
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
