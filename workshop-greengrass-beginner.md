# Workshop Greengrass

[AWS IoT Greengrass V2 for beginners (Korean)](https://catalog.us-east-1.prod.workshops.aws/workshops/0b21ceb7-2108-4a82-9e76-4c56d4b52db5/ko-KR)에 대해 설명합니다. 


## Cloud9 서버 준비

편의를 위해 Cloud9 서버를 준비합니다. 이때, 환경설정의 편의를 위해 "Ubuntu Server 18.04 LTS"을 선택합니다.

Credential을 등록합니다.

```c
export AWS_DEFAULT_REGION=ap-northeast-2
export AWS_ACCESS_KEY_ID=SAMPLE3IXN5TI2W4DP4A
export AWS_SECRET_ACCESS_KEY=0sampleabulrFsfsY0+gWeU3QciaBm5W4E2z123pc
```

## Greengrass V2 생성 및 Local 배포

### 1) Download the installer 

Greengrass installer를 아래 명령어로 다운로드 합니다. 

```c
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip 
unzip greengrass-nucleus-latest.zip -d GreengrassCore
```

상기 명령어로 다운로드할 경우에 GreengrassCore 폴더에는 아래와 같은 파일들이 있습니다. 

![noname](https://user-images.githubusercontent.com/52392004/182630947-38690340-239d-43a6-b9a6-cfbfb1ce7a94.png)




### 2) Run the installer 

아래 명령어로 IoT Core에 thing을 생성하고, greengrass에 등록합니다. 이때 생성되는 Core device name은 GreengrassQuickStartCore-18163f7ac3e이고, Thing group name은 GreengrassQuickStartGroup

```c
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar \
	--aws-region ap-northeast-2 \
	--thing-name GreengrassCore-18163f7ac3e \
	--thing-group-name GreengrassGroup \
	--component-default-user ggc_user:ggc_group \
	--provision true \
	--setup-system-service true \
	--deploy-dev-tools true
```	

```c
Provisioning AWS IoT resources for the device with IoT Thing Name: [GreengrassCore-18163f7ac3e]...
Creating new IoT policy "GreengrassV2IoTThingPolicy"
Creating keys and certificate...
Attaching policy to certificate...
Creating IoT Thing "GreengrassCore-18163f7ac3e"...
Attaching certificate to IoT thing...
Successfully provisioned AWS IoT resources for the device with IoT Thing Name: [GreengrassCore-18163f7ac3e]!
Adding IoT Thing [GreengrassCore-18163f7ac3e] into Thing Group: [GreengrassGroup]...
Successfully added Thing into Thing Group: [GreengrassGroup]
Setting up resources for aws.greengrass.TokenExchangeService ... 
IoT role policy "GreengrassTESCertificatePolicyGreengrassV2TokenExchangeRoleAlias" for TES Role alias not exist, creating policy...
Attaching TES role policy to IoT thing...
No managed IAM policy found, looking for user defined policy...
IAM policy named "GreengrassV2TokenExchangeRoleAccess" already exists. Please attach it to the IAM role if not already
Configuring Nucleus with provisioned resource details...
Downloading Root CA from "https://www.amazontrust.com/repository/AmazonRootCA1.pem"
Created device configuration
Successfully configured Nucleus with provisioned resource details!
Creating a deployment for Greengrass first party components to the thing group
Configured Nucleus to deploy aws.greengrass.Cli component
Creating user ggc_user 
ggc_user created 
Creating group ggc_group 
ggc_group created 
Added ggc_user to ggc_group 
Successfully set up Nucleus as a system service
```

이때 /greengrass/v2 폴더에는 아래와 같은 파일들이 생성됩니다. 

```c
$ ls /greengrass/v2/ -al
total 60
drwxr-xr-x 12 root root 4096 Aug  5 02:42 .
drwxr-xr-x  3 root root 4096 Aug  5 02:42 ..
drwx------  3 root root 4096 Aug  5 02:42 alts
drwxr-xr-x  2 root root 4096 Aug  5 02:43 bin
drwxr-xr-x  2 root root 4096 Aug  5 02:43 cli_ipc_info
drwx------  2 root root 4096 Aug  5 02:42 config
drwx------  3 root root 4096 Aug  5 02:43 deployments
srw-rw-rw-  1 root root    0 Aug  5 02:42 ipc.socket
drwx------  2 root root 4096 Aug  5 02:42 logs
drwxr-xr-x  5 root root 4096 Aug  5 02:42 packages
drwx------  4 root root 4096 Aug  5 02:42 plugins
-rw-r--r--  1 root root 1679 Aug  5 02:42 privKey.key
-rw-r--r--  1 root root 1188 Aug  5 02:42 rootCA.pem
drwxr-xr-x  2 root root 4096 Aug  5 02:42 telemetry
-rw-r--r--  1 root root 1224 Aug  5 02:42 thingCert.crt
drwxr-xr-x  2 root root 4096 Aug  5 02:42 work
```

GreengrassV2TokenExchangeRoleAccess인 policy 내용은 아래와 같습니다. 

```java
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams",
                "s3:GetBucketLocation"
            ],
            "Resource": "*"
        }
    ]
}
```

생성된 Core device에 대한 정보는 아래와 같습니다. 

<img width="1106" alt="image" src="https://user-images.githubusercontent.com/52392004/182634546-20bfe9f5-9c6b-4074-bf9b-9d72d2b7a340.png">


아래와 같이 greengrass service가 설치되어 있는것을 확인 할 수 있습니다. 

```c
$ sudo systemctl status greengrass.service
```

```c
● greengrass.service - Greengrass Core
   Loaded: loaded (/etc/systemd/system/greengrass.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2022-08-04 14:24:11 UTC; 10s ago
 Main PID: 970 (sh)
    Tasks: 22 (limit: 4915)
   CGroup: /system.slice/greengrass.service
           ├─970 /bin/sh /greengrass/v2/alts/current/distro/bin/loader
           └─988 java -Dlog.store=FILE -Dlog.store=FILE -Droot=/greengrass/v2 -jar /greengrass/v2/alts/current/distro/lib/Greengrass.jar --setup-system-servic
Aug 04 14:24:11 ip-172-31-19-59 systemd[1]: Started Greengrass Core.
Aug 04 14:24:11 ip-172-31-19-59 sh[970]: Greengrass root: /greengrass/v2
Aug 04 14:24:11 ip-172-31-19-59 sh[970]: JVM options: -Dlog.store=FILE -Droot=/greengrass/v2
Aug 04 14:24:11 ip-172-31-19-59 sh[970]: Nucleus options: --setup-system-service false
Aug 04 14:24:21 ip-172-31-19-59 sh[970]: Launching Nucleus...
```



Greengrass-cli가 설치되어 있는지 확인합니다. 

```c
$ /greengrass/v2/bin/greengrass-cli -V
bash: /greengrass/v2/bin/greengrass-cli: No such file or directory
```

만약 상기와 같이 설치되어 있지 않다면, [Greengrass CLI 설치](https://github.com/kyopark2014/iot-greengrass/blob/main/greengrass-cli.md)에 따라 Greengrass CLI를 설치합니다.


### 3) Local deployment를 위해 Receipe와 Artifact를 생성합니다.

- Recipe 생성

```c
mkdir -p ~/GGv2Dev/recipes
touch ~/GGv2Dev/recipes/com.example.HelloMqtt-1.0.0.json
```

이때, json 파일의 내용은 아래와 같습니다. 

```java
{
	"RecipeFormatVersion": "2020-01-25",
	"ComponentName": "com.example.HelloMqtt",
	"ComponentVersion": "1.0.0",
	"ComponentDescription": "My first AWS IoT Greengrass component.",
	"ComponentPublisher": "Amazon",
	"ComponentConfiguration": {
		"DefaultConfiguration": {
			"accessControl": {
				"aws.greengrass.ipc.mqttproxy": {
					"com.example.HelloMqtt:mqttproxy:1": {
						"policyDescription": "Allows access to publish to all AWS IoT Core topics.",
						"operations": [
							"aws.greengrass#PublishToIoTCore"
						],
						"resources": [
							"*"
						]
					}
				}
			}
		}
	},
	"Manifests": [{
		"Platform": {
			"os": "linux"
		},
		"Lifecycle": {
			"Install": {
				"RequiresPrivilege": true,
				"Script": "sudo pip3 install awsiotsdk"
			},
			"Run": "python3 {artifacts:path}/hello_mqtt.py"
		}
	}]
}
```

- Artifact는 아래와 같이 생성합니다.

```c
mkdir -p ~/GGv2Dev/artifacts/com.example.HelloMqtt/1.0.0
touch ~/GGv2Dev/artifacts/com.example.HelloMqtt/1.0.0/hello_mqtt.py
```

이때 hello_mqtt.py의 내용은 아래와 같습니다.

```pytion
import json
import time
import os
import random

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

if __name__ == '__main__':
    ipc_client = awsiot.greengrasscoreipc.connect()

    while True:
        telemetry_data = {
            "timestamp": int(round(time.time() * 1000)),
            "battery_level": random.randrange(98, 101),
            "location": {
                "longitude": round(random.uniform(101.0, 120.0),2),
                "latitude": round(random.uniform(30.0, 40.0),2),
            },
        }

        op = ipc_client.new_publish_to_iot_core()
        op.activate(model.PublishToIoTCoreRequest(
            topic_name="ggv2/{}/telemetry".format(os.getenv("AWS_IOT_THING_NAME")),
            qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(telemetry_data).encode(),
        ))
        try:
            result = op.get_response().result(timeout=1.0)
            print("successfully published message:", result)
        except Exception as e:
            print("failed to publish message:", e)

        time.sleep(5)
```

아래 명령어로 Local deployment를 수행합니다.
 
```c 
 sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir ~/GGv2Dev/recipes \
  --artifactDir ~/GGv2Dev/artifacts \
  --merge "com.example.HelloMqtt=1.0.0"
```
```c
Aug 03, 2022 3:31:46 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Aug 03, 2022 3:31:46 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Local deployment submitted! Deployment Id: 4a340ea0-0aad-4c7f-a9de-55bda9cad0f5
```

"com.example.HelloMqtt"가 잘 등록되어 있음을 아래와 같이 확인 합니다. 이때 state가 "RUNNING"이어야 합니다. 

```c
$ sudo /greengrass/v2/bin/greengrass-cli component list
Jun 14, 2022 8:56:49 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Jun 14, 2022 8:56:49 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Components currently running in Greengrass:
Component Name: FleetStatusService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: TelemetryAgent
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: com.example.HelloMqtt
    Version: 1.0.0
    State: RUNNING
    Configuration: {"accessControl":{"aws.greengrass.ipc.mqttproxy":{"com.example.HelloMqtt:mqttproxy:1":{"operations":["aws.greengrass#PublishToIoTCore"],"policyDescription":"Allows access to publish to all AWS IoT Core topics.","resources":["*"]}}}}
Component Name: DeploymentService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: aws.greengrass.Nucleus
    Version: 2.5.6
    State: FINISHED
    Configuration: {"awsRegion":"ap-northeast-2","componentStoreMaxSizeBytes":"10000000000","deploymentPollingFrequencySeconds":"15","envStage":"prod","fleetStatus":{"periodicStatusPublishIntervalSeconds":86400.0},"greengrassDataPlanePort":"8443","httpClient":{},"iotCredEndpoint":"c198kakbg1m4dh.credentials.iot.ap-northeast-2.amazonaws.com","iotDataEndpoint":"anr3wll34rul5-ats.iot.ap-northeast-2.amazonaws.com","iotRoleAlias":"GreengrassV2TokenExchangeRoleAlias","jvmOptions":"-Dlog.store=FILE","logging":{},"mqtt":{"spooler":{}},"networkProxy":{"proxy":{}},"platformOverride":{},"runWithDefault":{"posixShell":"sh","posixUser":"ggc_user:ggc_group"},"telemetry":{}}
Component Name: aws.greengrass.Cli
    Version: 2.5.6
    State: RUNNING
    Configuration: {"AuthorizedPosixGroups":null,"AuthorizedWindowsGroups":null}
Component Name: UpdateSystemPolicyService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
```

동작확인을 위해 [MQTT test client]로 이동합니다.

https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/test

아래처럼 [Topic filter]에 "ggv2/#"이라고 입력합니다. 

![noname](https://user-images.githubusercontent.com/52392004/173702204-0803c46e-9eab-4c44-8f2e-6e3b9f8f374a.png)

아래와 같이 com.example.HelloMqtt가 보낸 메시지를 확인 할 수 있습니다.

![image](https://user-images.githubusercontent.com/52392004/173701949-c482d009-1e75-4af1-9a46-393316bd4dd2.png)


## Troubleshooting: state가 "BROKEN" 인 경우

아래와 같이 com.example.HelloMqtt의 state가 BROKEN으로 확인되었습니다.

```c
$ sudo /greengrass/v2/bin/greengrass-cli component list
Jun 14, 2022 8:37:50 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Jun 14, 2022 8:37:51 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Components currently running in Greengrass:
Component Name: FleetStatusService
    Version: null
    State: RUNNING
    Configuration: null
Component Name: UpdateSystemPolicyService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: aws.greengrass.Nucleus
    Version: 2.5.6
    State: FINISHED
    Configuration: {"awsRegion":"us-east-1","componentStoreMaxSizeBytes":"10000000000","deploymentPollingFrequencySeconds":"15","envStage":"prod","fleetStatus":{"periodicStatusPublishIntervalSeconds":86400.0},"greengrassDataPlanePort":"8443","httpClient":{},"iotCredEndpoint":"c198kakbg1m4dh.credentials.iot.us-east-1.amazonaws.com","iotDataEndpoint":"anr3wll34rul5-ats.iot.us-east-1.amazonaws.com","iotRoleAlias":"GreengrassV2TokenExchangeRoleAlias","jvmOptions":"-Dlog.store=FILE","logging":{},"mqtt":{"spooler":{}},"networkProxy":{"proxy":{}},"platformOverride":{},"runWithDefault":{"posixShell":"sh","posixUser":"ggc_user:ggc_group"},"telemetry":{}}
Component Name: TelemetryAgent
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: aws.greengrass.Cli
    Version: 2.5.6
    State: RUNNING
    Configuration: {"AuthorizedPosixGroups":null,"AuthorizedWindowsGroups":null}
Component Name: DeploymentService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: com.example.HelloMqtt
    Version: 1.0.0
    State: BROKEN
    Configuration: {"accessControl":{"aws.greengrass.ipc.mqttproxy":{"com.example.HelloMqtt:mqttproxy:1":{"operations":["aws.greengrass#PublishToIoTCore"],"policyDescription":"Allows access to publish to all AWS IoT Core topics.","resources":["*"]}}}}
```

이때, 아래와 같이 "user root is not allowed to execute"와 같은 문제를 가지고 있습니다.

```c
$ sudo tail -f /greengrass/v2/logs/com.example.HelloMqtt.log
2022-06-14T20:35:35.791Z [WARN] (Copier) com.example.HelloMqtt: stderr. Sorry, user root is not allowed to execute '/bin/sh -c python3 /greengrass/v2/packages/artifacts/com.example.HelloMqtt/1.0.0/hello_mqtt.py' as ggc_user:ggc_group on ip-172-31-73-73.ec2.internal.. {scriptName=services.com.example.HelloMqtt.lifecycle.Run, serviceName=com.example.HelloMqtt, currentState=RUNNING}
2022-06-14T20:35:35.794Z [INFO] (Copier) com.example.HelloMqtt: Run script exited. {exitCode=1, serviceName=com.example.HelloMqtt, currentState=RUNNING}
2022-06-14T20:35:35.796Z [INFO] (pool-2-thread-23) com.example.HelloMqtt: shell-runner-start. {scriptName=services.com.example.HelloMqtt.lifecycle.Run, serviceName=com.example.HelloMqtt, currentState=STARTING, command=["python3 /greengrass/v2/packages/artifacts/com.example.HelloMqtt/1.0.0/hello_mq..."]}
2022-06-14T20:35:35.807Z [WARN] (Copier) com.example.HelloMqtt: stderr. Sorry, user root is not allowed to execute '/bin/sh -c python3 /greengrass/v2/packages/artifacts/com.example.HelloMqtt/1.0.0/hello_mqtt.py' as ggc_user:ggc_group on ip-172-31-73-73.ec2.internal.. {scriptName=services.com.example.HelloMqtt.lifecycle.Run, serviceName=com.example.HelloMqtt, currentState=RUNNING}
2022-06-14T20:35:35.810Z [INFO] (Copier) com.example.HelloMqtt: Run script exited. {exitCode=1, serviceName=com.example.HelloMqtt, currentState=RUNNING}
```

[User root is not allowed to execute](https://docs.aws.amazon.com/greengrass/v2/developerguide/troubleshooting.html#user-not-allowed-to-execute)에 따라 아래 명령어로 root의 permission을 확인합니다. 

```c
$ sudo cat /etc/sudoers
```
이때 퍼미션이 아래와 같음을 알수 있습니다.

```c
root    ALL=(ALL)   ALL
```

아래와 같이 변경해줍니다. 

```c
root    ALL=(ALL:ALL)   ALL
```


"com.example.HelloMqtt"을 아래 명령어로 삭제합니다. 

```c
$ sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.example.HelloMqtt"
Jun 14, 2022 9:09:22 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Jun 14, 2022 9:09:23 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Local deployment submitted! Deployment Id: 1f94aac2-6909-42cd-8d0d-6114bf096910
```


아래와 같이 삭제를 확인합니다.

```c
$ sudo /greengrass/v2/bin/greengrass-cli component list
Jun 14, 2022 9:09:53 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Jun 14, 2022 9:09:53 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Components currently running in Greengrass:
Component Name: FleetStatusService
    Version: null
    State: RUNNING
    Configuration: null
Component Name: UpdateSystemPolicyService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: aws.greengrass.Nucleus
    Version: 2.5.6
    State: FINISHED
    Configuration: {"awsRegion":"us-east-1","componentStoreMaxSizeBytes":"10000000000","deploymentPollingFrequencySeconds":"15","envStage":"prod","fleetStatus":{"periodicStatusPublishIntervalSeconds":86400.0},"greengrassDataPlanePort":"8443","httpClient":{},"iotCredEndpoint":"c198kakbg1m4dh.credentials.iot.us-east-1.amazonaws.com","iotDataEndpoint":"anr3wll34rul5-ats.iot.us-east-1.amazonaws.com","iotRoleAlias":"GreengrassV2TokenExchangeRoleAlias","jvmOptions":"-Dlog.store=FILE","logging":{},"mqtt":{"spooler":{}},"networkProxy":{"proxy":{}},"platformOverride":{},"runWithDefault":{"posixShell":"sh","posixUser":"ggc_user:ggc_group"},"telemetry":{}}
Component Name: TelemetryAgent
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: aws.greengrass.Cli
    Version: 2.5.6
    State: RUNNING
    Configuration: {"AuthorizedPosixGroups":null,"AuthorizedWindowsGroups":null}
Component Name: DeploymentService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
```

다시 재실행합니다. 

```c
$ sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/GGv2Dev/recipes --artifactDir ~/GGv2Dev/artifacts --merge "com.example.HelloMqtt=1.0.0"  
Jun 14, 2022 9:10:49 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Jun 14, 2022 9:10:50 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Local deployment submitted! Deployment Id: 88f90d1a-af2c-474d-8275-6379cd3268c1
```

아래와 같이 component list를 확인하면 "com.example.HelloMqtt"가 정상적으로 RUNNING 하고 있음을 알수 있습니다. 

```c
$ sudo /greengrass/v2/bin/greengrass-cli component list
Jun 14, 2022 9:11:16 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Jun 14, 2022 9:11:17 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Components currently running in Greengrass:
Component Name: FleetStatusService
    Version: null
    State: RUNNING
    Configuration: null
Component Name: UpdateSystemPolicyService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: aws.greengrass.Nucleus
    Version: 2.5.6
    State: FINISHED
    Configuration: {"awsRegion":"us-east-1","componentStoreMaxSizeBytes":"10000000000","deploymentPollingFrequencySeconds":"15","envStage":"prod","fleetStatus":{"periodicStatusPublishIntervalSeconds":86400.0},"greengrassDataPlanePort":"8443","httpClient":{},"iotCredEndpoint":"c198kakbg1m4dh.credentials.iot.us-east-1.amazonaws.com","iotDataEndpoint":"anr3wll34rul5-ats.iot.us-east-1.amazonaws.com","iotRoleAlias":"GreengrassV2TokenExchangeRoleAlias","jvmOptions":"-Dlog.store=FILE","logging":{},"mqtt":{"spooler":{}},"networkProxy":{"proxy":{}},"platformOverride":{},"runWithDefault":{"posixShell":"sh","posixUser":"ggc_user:ggc_group"},"telemetry":{}}
Component Name: TelemetryAgent
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: aws.greengrass.Cli
    Version: 2.5.6
    State: RUNNING
    Configuration: {"AuthorizedPosixGroups":null,"AuthorizedWindowsGroups":null}
Component Name: DeploymentService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: com.example.HelloMqtt
    Version: 1.0.0
    State: RUNNING
    Configuration: {"accessControl":{"aws.greengrass.ipc.mqttproxy":{"com.example.HelloMqtt:mqttproxy:1":{"operations":["aws.greengrass#PublishToIoTCore"],"policyDescription":"Allows access to publish to all AWS IoT Core topics.","resources":["*"]}}}}
```    
