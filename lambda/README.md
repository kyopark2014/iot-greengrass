# Lambda Component 만들기

여기서는 python과 node.js로 lambda component를 만드는 방법에 대해 설명합니다. 

## Python으로 Lambda Component 생성하기

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

아래와 같이 "example-lambda-python" 동작을 확인합니다. 

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


## Node.JS로 Lambda Component 생성하기 

1) Python 생성과 같은 방식으로 "example-lambda-nodejs"라는 lambda 함수를 생성합니다. 이때, Runtime은 "Node.js 14.x"을 선택합니다. 

2) index.js를 아래처럼 업데이트 합니다.
```java
const iotsdk = require('aws-greengrass-core-sdk');

const GROUP_ID = process.env.GROUP_ID;
const THING_NAME = process.env.AWS_IOT_THING_NAME; 
const THING_ARN = process.env.AWS_IOT_THING_ARN; 

exports.handler = async (event) => {
    console.log('## ENVIRONMENT VARIABLES: ' + JSON.stringify(process.env));
    console.log('## EVENT: ' + JSON.stringify(event)); 
    
    const response = {
        statusCode: 200,
        body: JSON.stringify(event),
    };
    return response;
};
```
3) AWS SDK를 설치합니다. 

```c
npm init -y 
npm install aws-greengrass-core-sdk
```

4) 아래와 같이 압축하여 lambda함수를 업데이트 합니다. 

```c
zip -r deploy.zip *
```

5) 아래와 같이 [Component source]로 "Import Lambda function"을 선택하고, [lambda function]으로 "example-lambda-nodejs"을 선택합니다. 이때 [lambda function version]도 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/183247263-b137f5f8-df6b-4fc6-b097-cddfb22ced32.png)

6) [Event Sources]에서 Topic으로 "core/topic"을 입력하고, Type으로 "AWS IoT Core MQTT"을 선택합니다. 이후 하단에서 [Create component]를 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/183247489-e0ebfd95-84f1-42dd-bbed-5eca16aca73a.png)

7) Python 방식과 동일하게 deploy를 진행합니다. 

10) 실행결과의 확인 

아래와 같이 "example-lambda-nodejs" 동작을 확인합니다. 

```java
sudo tail -f /greengrass/v2/logs/example-lambda-nodejs.log 
```

```java
2022-08-06T12:00:49.001Z [INFO] (pool-2-thread-37) example-lambda-nodejs: START RequestId: 5750b6e8-63f6-441b-ba2d-3cae3fe339e9. {serviceInstance=0, serviceName=example-lambda-nodejs, currentState=RUNNING}
2022-08-06T12:00:49.002Z [INFO] (pool-2-thread-37) example-lambda-nodejs: ## ENVIRONMENT VARIABLES: {
   "AWS_GREENGRASS_LAMBDA_ARTIFACT_PATH":"/greengrass/v2/packages/artifacts-unarchived/example-lambda-nodejs/8.0.0/lambda-artifact",
   "AWS_GREENGRASS_LAMBDA_CONTAINER_PARAMS":"{\"devices\":{},\"memorySize\":16384,\"mountROSysfs\":false,\"volumes\":{}}",
   "AWS_DEFAULT_REGION":"ap-northeast-2",
   "GG_ROOT_CA_PATH":"/greengrass/v2/rootCA.pem",
   "INVOCATION_ID":"samplecc802eb41a0b5cd61edb5381034",
   "AWS_CONTAINER_AUTHORIZATION_TOKEN":"SAMPLEWTTWEBRPKZA",
   "AWS_GREENGRASS_LAMBDA_CONTAINER_MODE":"GreengrassContainer",
   "AWS_REGION":"ap-northeast-2",
   "AWS_GREENGRASS_LAMBDA_STATUS_TIMEOUT_SECONDS":"60",
   "GG_DAEMON_PORT":"35287",
   "MY_FUNCTION_ARN":"arn:aws:lambda:ap-northeast-2:123456789012:function:example-lambda-nodejs:9",
   "NODE_PATH":"/lambda/:/runtime/nodejs/node_modules:/lambda/node_modules",
   "HOME":"/home/ggc_user",
   "AWS_GREENGRASS_LAMBDA_WORKER_ID":"hXI6TmoR5oLwzFBL-R7DfycEpHbNQwxwx1w2Phfsifc",
   "AWS_GG_NUCLEUS_DOMAIN_SOCKET_FILEPATH":"/greengrass/v2/ipc.socket",
   "JAVA_HOME":"/usr/lib/jvm/java-11-openjdk-amd64",
   "SHADOW_FUNCTION_ARN":"arn:aws:lambda:::function:GGShadowService",
   "AWS_GG_NUCLEUS_DOMAIN_SOCKET_FILEPATH_FOR_COMPONENT":"/socket/greengrassv2_ipc.sock",
   "PATH":"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/lambda/:/usr/bin:/usr/local/bin",
   "LANG":"C.UTF-8",
   "AWS_GREENGRASS_LAMBDA_LINUX_PROCESS_PARAMS":"{\"user\": \"ggc_user\",\"group\": \"ggc_group\"}",
   "PWD":"/greengrass/v2/work/example-lambda-nodejs",
   "GGC_VERSION":"2.7.0",
   "AWS_GREENGRASS_LAMBDA_RUNTIME":"nodejs14.x",
   "AWS_IOT_THING_NAME":"GreengrassCore-18163f7ac3e",
   "AWS_GREENGRASS_LAMBDA_PARAMS":"{\"EnvironmentVariables\":{}}",
   "AWS_GREENGRASS_LAMBDA_EXEC_ARGS":"[\"nodejs14.x\",\"/runtime/nodejs/lambda_nodejs_runtime.js\",\"--handler=index.handler\"]",
   "ROUTER_FUNCTION_ARN":"arn:aws:lambda:::function:GGRouter",
   "ENCODING_TYPE":"json",
   "LOG_LEVEL":"INFO",
   "AWS_GREENGRASS_LAMBDA_FUNCTION_HANDLER":"index.handler",
   "JOURNAL_STREAM":"9:73656",
   "AWS_GREENGRASS_LAMBDA_ENCODING_TYPE":"json",
   "AWS_CONTAINER_CREDENTIALS_FULL_URI":"http://localhost:38251/2016-11-01/credentialprovider/",
   "AWS_GREENGRASS_LAMBDA_ARN":"arn:aws:lambda:ap-northeast-2:677146750822:function:example-lambda-nodejs:9",
   "SVCUID":"GKU0EWTTWEBRPKZA",
   "AWS_GREENGRASS_LAMBDA_MESSAGE_PORT":"35287",
   "LOG_DIR":"/greengrass/v2/work/example-lambda-nodejs/logs/0",
   "AWS_GREENGRASS_LAMBDA_RUNTIME_PATH":"/greengrass/v2/packages/artifacts-unarchived/aws.greengrass.LambdaRuntimes/2.0.8/runtime/",
   "AWS_GG_RESOURCE_PREFIX":"/",
   "GGC_MAX_INTERFACE_VERSION":"1.5",
   "SECRETS_MANAGER_FUNCTION_ARN":"arn:aws:lambda:::function:GGSecretManager:1",
   "IPC_SOCK_FILE":"/greengrass_ipc.sock",
   "_GG_LOG_FD_TRACE":"6",
   "_GG_LOG_FD_DEBUG":"3",
   "_GG_LOG_FD_INFO":"1",
   "_GG_LOG_FD_WARN":"4",
   "_GG_LOG_FD_ERROR":"2",
   "_GG_LOG_FD_FATAL":"5"
}"."{
   serviceInstance=0,
   "serviceName=example-lambda-nodejs",
   "currentState=RUNNING"
}
2022-08-06T12:00:49.002Z [INFO] (pool-2-thread-37) example-lambda-nodejs: ## EVENT: {"msg":"hello.world","date":"2022-08-06 12:00:48.985047"}. {serviceInstance=0, serviceName=example-lambda-nodejs, currentState=RUNNING}
2022-08-06T12:00:49.002Z [INFO] (pool-2-thread-37) example-lambda-nodejs: End RequestId: 5750b6e8-63f6-441b-ba2d-3cae3fe339e9. {serviceInstance=0, serviceName=example-lambda-nodejs, currentState=RUNNING}
```


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

## Troubleshooting 

Node.JS의 경우에 아래와 같은 "exec: "nodejs14.x": executable file not found"에러가 발생할 수 있습니다. 


2022-08-06T10:16:13.857Z [WARN] (Copier) example-lambda-nodejs: stderr. 2022/08/06 10:16:13 unable to create start process: failed to run container sandbox: container_linux.go:380: starting container process caused: exec: "nodejs14.x": executable file not found in $PATH. {scriptName=services.example-lambda-nodejs.lifecycle.startup.script, serviceInstance=0, serviceName=example-lambda-nodejs, currentState=STARTING}

이때, [NodeJS 12.x: Not found Error in AWS Greengrass](https://stackoverflow.com/questions/64861329/nodejs-12-x-not-found-error-in-aws-greengrass)을 
이때, exec: "nodejs14.x": executable file not foundㅊㅏㅁ조하여 
이때, exec: "nodejs14.x": executable file not fou

## Reference

[Tutorial creating hello world greengrass Lambda (in Python)](https://www.youtube.com/watch?v=jvQsygmzov0) - V1.0
