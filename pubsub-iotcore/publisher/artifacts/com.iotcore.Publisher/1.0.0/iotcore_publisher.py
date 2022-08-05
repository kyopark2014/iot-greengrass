import time
import datetime
import json

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client

from awsiot.greengrasscoreipc.model import (
    QOS,
    PublishToIoTCoreRequest
)

TIMEOUT = 10

ipc_client = awsiot.greengrasscoreipc.connect()
                    
topic = "core/topic"
cnt = 1

while True: 
    message = {"timestamp": str(datetime.datetime.now()),
               "value": cnt}
    message_json = json.dumps(message).encode('utf-8')
    cnt = cnt + 1
    qos = QOS.AT_LEAST_ONCE

    request = PublishToIoTCoreRequest()
    request.topic_name = topic
    request.payload = bytes(message, "utf-8")
    request.qos = qos
    operation = ipc_client.new_publish_to_iot_core()
    operation.activate(request)
    future_response = operation.get_response()
    future_response.result(TIMEOUT)

    print(f"publish: {message_json}")
