#
#  enable TLS client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
import paho.mqtt.client as paho
from paho import mqtt
import json

global alarmDict 
alarmDict = {}

global stateDict 
stateDict = {"timenow" : [], "set_time" : [], "take_act" : [], "take_state" : [], "pillbox_info" : [], "next_pillbox" : []}
# 테스트용 전송 json 메세지, 각 시간별 값을 받아내어 보내도록 수정 해야함
exStateDict = {"timenow" : [13,50,30], "set_time" : [7,20,13,15,19,25,23,50], "take_act" : [1,1,1,1], "take_state" : [0,0,0,0], "pillbox_info" : [1,2,3,3,1,2,3], "next_pillbox" : [4]}

# 글로벌 토픽 변수를 만들어서 받은 토픽으로 처리한다
# 먼저 상위 토픽에서 userID를 받은 후 그것을 기준으로 topic을 만들어서 mqtt통신
global testUserIDTopic
testUserIDTopic = "Sub/"


global checkNum
checkNum = 0

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    # 나중에 qos도 신경써야 할 것
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    global testUserIDTopic
    data = dict(
        topic=msg.topic,
        payload=msg.payload.decode()
    )
    deviceInfo = ["type", "userID", "deviceID"]
    pillStateInfo = ["type", "userID", "deviceID", "dosing number", "alarm Time", "act", "take info", "taking Time"]
    values = json.loads(data['payload'])
    
    '''
    전송용 프로토콜 형태로 만든 후 CABINET으로 전송처리해주세요

  
    현재시간 0x7E 시 분 초
    알람시간 0x7C 시 분 시 분 시 분 시 분
    알람활성 0x7B 1 0 1 0
    복용상태 0x7F 0 복용예정 1 미복용 5 정보없음 6복용 
    약통불빛 0x6B 0 복용예정 1 복용 2 미복용 3 지연복용
    약통위치 0x6C 5
    '''

    '''
    타입 1: 처음 연결 되었을때 보내는 값
    타입 2: 약 먹었을때 보내는 값
    타입 5: 리셋되거나 모드버튼을 눌러 전체적으로 보낼때 쓰는 값
    '''

    for i in range(0,3) :
        print(" ")

    print('topic type : ' + str(type(data["topic"])))
    print('topic : ' + data["topic"])

    print('value type : ' + str(type(values)))
    print('json to dic : ' + str(values))

    if (values['type'] == "1") :
        for i in deviceInfo :
            print( i + " : " + str(values[i]) )
            if (i == 'userID') :
                testUserIDTopic += str(values[i])
                print(i + " devicetopic : " + testUserIDTopic)
    elif (values['type'] == "2") :
        for i in pillStateInfo :
            print( i + " : " + str(values[i]) )
    elif (values['type'] == "5") :
        for i in pillStateInfo :
            print( i + " : " + str(values[i]) )

    for i in range(0,3) :
        print(" ")

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("healthall", "0533848590")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("ee7b50ae60a9430e8a1801ee64d51efc.s2.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("Sub/#", qos=1)

if (testUserIDTopic != "Sub/") :
    print("testUserIDTopic : " + testUserIDTopic)
    client.subscribe(testUserIDTopic, qos=1)




# a single publish, this can also be done in loops, etc.
# client.publish("Pub/test", payload="hot", qos=1)
client.publish("Pub/test", payload=exStateDict, qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()