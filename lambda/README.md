# Lambda Component 만들기

여기서는 python과 node.js로 lambda component를 만드는 방법에 대해 설명합니다. 

## Python을 생성하기 

1) [[AWS Lambda] - [Functions]](https://ap-northeast-2.console.aws.amazon.com/lambda/home?region=ap-northeast-2#/functions)에서 [Create function]을 선택하고, [function name]에 "example-lambda-python"을 입력하고 [Runtime]으로 적절한 Python 라이브러리를 선택한 후에 [Create function]을 선택합니다. 

2) event로그를 찍도록 ["lambda_function.py"을 업데이트](https://github.com/kyopark2014/iot-greengrass/blob/main/lambda/example-lambda-python/lambda_function.py) 합니다. 

```python
import json

def lambda_handler(event, context):  
    print('## EVENT') 
    print(event) 
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

3) 아래처럼 [Versions]에서 버전을 정의 합니다. 

![image](https://user-images.githubusercontent.com/52392004/182875433-879f8e0a-331b-4435-ae31-3d13061bed88.png)

4) Alias를 선택하여 아래처럼 [Name]으로 "v1"을 지정하고, [Version]은 1을 선택합니다. 

![image](https://user-images.githubusercontent.com/52392004/182875925-48bdff5a-9d72-4ec0-9847-a5e77ee0821a.png)

5) [[Greengrass devices] - [Components]](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/components)에서 [Create Component]를 선택합니다.

6) 아래와 같이 [Component source]로 "Import Lambda function"을 선택하고, [lambda function]으로 "example-lambda-python"을 선택합니다. 이때 [lambda function version]도 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/183247347-52f6ccdb-e706-4824-9df2-a9659349635a.png)

7) [Event Sources]에서 Topic으로 "core/topic"을 입력하고, Type으로 "AWS IoT Core MQTT"을 선택합니다. 이후 하단에서 [Create component]를 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/183247489-e0ebfd95-84f1-42dd-bbed-5eca16aca73a.png)

8) 아래와 같이 생성한 "example-lambda-python"을 선택한 후에 상단의 [Deploy]를 선택합니다. 

![image](https://user-images.githubusercontent.com/52392004/183247543-45e364f0-c63a-4bf4-87ff-fca8829e41ce.png)

9) 아래와 같이 Deployment를 선택하고 [Next]를 선택합니다. 계속 Next를 선택하여 Deploy 합니다. 

![image](https://user-images.githubusercontent.com/52392004/183247597-40027dbb-1c8a-483e-9cb4-4c6b9e173a8c.png)

10) 실행결과의 확인 

아래와 같이 "example-lambda-python"에서 동작을 확인합니다. 

```java
sudo tail -f /greengrass/v2/logs/example-lambda-python.log 
```

```java
2022-08-06T11:47:33.190Z [INFO] (pool-2-thread-44) example-lambda-python: lambda_function.py:4,## EVENT. {serviceInstance=0, serviceName=example-lambda-python, currentState=RUNNING}
2022-08-06T11:47:33.190Z [INFO] (pool-2-thread-44) example-lambda-python: lambda_function.py:5,{'msg': 'hello.world', 'date': '2022-08-06 11:47:33.178276'}. {serviceInstance=0, serviceName=example-lambda-python, currentState=RUNNING}
2022-08-06T11:47:33.196Z [INFO] (pool-2-thread-44) example-lambda-python: lambda_function.py:4,## EVENT. {serviceInstance=0, serviceName=example-lambda-python, currentState=RUNNING}
2022-08-06T11:47:33.199Z [INFO] (pool-2-thread-44) example-lambda-python: lambda_function.py:5,{'msg': 'hello.world', 'date': '2022-08-06 11:47:33.178276'}. {serviceInstance=0, serviceName=example-lambda-python, currentState=RUNNING}
2022-08-06T11:47:38.186Z [INFO] (pool-2-thread-44) example-lambda-python: lambda_function.py:4,## EVENT. {serviceInstance=0, serviceName=example-lambda-python, currentState=RUNNING}
2022-08-06T11:47:38.186Z [INFO] (pool-2-thread-44) example-lambda-python: lambda_function.py:5,{'timestamp': '2022-08-06 11:47:38.184188', 'value': 1028.39}. {serviceInstance=0, serviceName=example-lambda-python, currentState=RUNNING}
```

아래와 같이 component list를 확인합니다. 

```java
sudo /greengrass/v2/bin/greengrass-cli component list
```
```java
Component Name: example-lambda-python
    Version: 8.0.0
    State: RUNNING
    Configuration: {"containerMode":"GreengrassContainer","containerParams":{"devices":{},"memorySize":16384.0,"mountROSysfs":false,"volumes":{}},"inputPayloadEncodingType":"json","lambdaExecutionParameters":{"EnvironmentVariables":{}},"maxIdleTimeInSeconds":60.0,"maxInstancesCount":100.0,"maxQueueSize":1000.0,"pinned":true,"pubsubTopics":{"0":{"topic":"core/topic","type":"IOT_CORE"},"1":{"topic":"local/topic","type":"PUB_SUB"},"2":{"topic":"#","type":"IOT_CORE"}},"statusTimeoutInSeconds":60.0,"timeoutInSeconds":3.0}
```


## Node.JS




![noname](https://user-images.githubusercontent.com/52392004/183247263-b137f5f8-df6b-4fc6-b097-cddfb22ced32.png)



3) greengrasssdk를 다운로드합니다.

```c
git clone https://github.com/aws/aws-greengrass-core-sdk-python 
```

5) lambda 함수에 업로드하기 위하여 압축을 합니다. 

```c
cd example-lambda-python
zip -r deploy.zip *
```
7) 상단 오른쪽의 [Upload from]에서 [.zip]을 선택한 후에 "deploy.zip"을 선택하여 업로드 합니다. 

아래와 같이 component list를 확인합니다. 

```java
sudo /greengrass/v2/bin/greengrass-cli component list
```
```java
Component Name: example-lambda-nodejs
    Version: 8.0.0
    State: RUNNING
    Configuration: {"containerMode":"GreengrassContainer","containerParams":{"devices":{},"memorySize":16384.0,"mountROSysfs":false,"volumes":{}},"inputPayloadEncodingType":"json","lambdaExecutionParameters":{"EnvironmentVariables":{}},"maxIdleTimeInSeconds":60.0,"maxInstancesCount":100.0,"maxQueueSize":1000.0,"pinned":true,"pubsubTopics":{"0":{"topic":"core/topic","type":"IOT_CORE"}},"statusTimeoutInSeconds":60.0,"timeoutInSeconds":3.0}
```    
    

## Reference

[Tutorial creating hello world greengrass Lambda (in Python)](https://www.youtube.com/watch?v=jvQsygmzov0) - V1.0
