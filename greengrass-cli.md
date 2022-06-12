# Greengrass CLI 설치 

[Install the Greengrass CLI](https://docs.aws.amazon.com/greengrass/v2/developerguide/install-gg-cli.html)을 따라 아래와 같이 Greengrass cli를 설치합니다. 



### To deploy the Greengrass CLI component (console)

1) [AWS IoT Console] - [Greengrass devices] - [Component]로 진입하여 "Public compenents"중에 "aws.greengrass.Cli"을 선택합니다.  

https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/components/public

2) [aws.greengrass.Cli]에서 아래처럼 "Deploy"를 선택하여 

![noname](https://user-images.githubusercontent.com/52392004/173242333-d07efb54-4821-4bbc-8a40-4a8595d7f3d1.png)

3) [Create new deployment]를 선택합니다.

![noname](https://user-images.githubusercontent.com/52392004/173242582-188ccb81-cd32-4c91-b72e-56d97c388a0b.png)

4) [Specify target]에서 [Target type]으로 "Thing group"을 선택하고, [Target name]으로 생성한 group 이름을 선택합니다. 여기서는 기 생성한 "GreengrassGroup"을 선택합니다. 이후 [Next]를 선택합니다. 


![noname](https://user-images.githubusercontent.com/52392004/173243225-633c987f-e82d-4d79-979f-364616661c03.png)



5) 이후 [Select components]에 "aws.greengrass.Cli"가 선택되었는지 확인 후, [Next]를 선택합니다. 

6) [Configure components]에서 Selected components에 "aws.greengrass.Cli" 확인후 [Next]를 선택합니다. 

7) [Configure advanced settings - optional에서도 마찬가지로 [Next]를 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/173242931-885f4d90-bc64-4251-af93-51b4904b28f3.png)

8) [Review]후에 [Deploy]를 선택합니다.  

이후 아래처럼 Deployment가 실행되어서, device가 online이라면 설치가 수행됩니다. 

![image](https://user-images.githubusercontent.com/52392004/173243274-7df3c3ee-6fd2-4280-9234-4959c775a20a.png)


9) [IoT job]을 선택하여 들어가면 아래처럼 

![noname](https://user-images.githubusercontent.com/52392004/173243420-f67479d9-0e1c-4fb9-af7d-b8ec5eca09bc.png)

```c
$ /greengrass/v2/bin/greengrass-cli -V
bash: /greengrass/v2/bin/greengrass-cli: No such file or directory
```

설치가 잘되면 아래처럼 확인이 가능합니다. 

```c
$ /greengrass/v2/bin/greengrass-cli help
Usage: greengrass-cli [-hV] [--ggcRootPath=<ggcRootPath>] [COMMAND]
Greengrass command line interface

      --ggcRootPath=<ggcRootPath>
                  The AWS IoT Greengrass V2 root directory.
  -h, --help      Show this help message and exit.
  -V, --version   Print version information and exit.
Commands:
  help                Show help information for a command.
  component           Retrieve component information and stop or restart
                        components.
  deployment          Create local deployments and retrieve deployment status.
  logs                Analyze Greengrass logs.
  get-debug-password  Generate a password for use with the HTTP debug view
                        component.
```                        

아래처럼 Greengrass Core 디바이스의 components 목록을 확인 할 수 있습니다. 

```c
$ sudo /greengrass/v2/bin/greengrass-cli component list

Jun 12, 2022 4:46:32 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Jun 12, 2022 4:46:32 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Components currently running in Greengrass:
Component Name: FleetStatusService
    Version: null
    State: RUNNING
    Configuration: null
Component Name: aws.greengrass.Nucleus
    Version: 2.5.6
    State: FINISHED
    Configuration: {"awsRegion":"ap-northeast-2","componentStoreMaxSizeBytes":"10000000000","deploymentPollingFrequencySeconds":"15","envStage":"prod","fleetStatus":{"periodicStatusPublishIntervalSeconds":86400.0},"greengrassDataPlanePort":"8443","httpClient":{},"iotCredEndpoint":"c198kakbg1m4dh.credentials.iot.ap-northeast-2.amazonaws.com","iotDataEndpoint":"anr3wll34rul5-ats.iot.ap-northeast-2.amazonaws.com","iotRoleAlias":"GreengrassV2TokenExchangeRoleAlias","jvmOptions":"-Dlog.store=FILE","logging":{},"mqtt":{"spooler":{}},"networkProxy":{"proxy":{}},"platformOverride":{},"runWithDefault":{"posixUser":"ggc_user:ggc_group"},"telemetry":{}}
Component Name: DeploymentService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: UpdateSystemPolicyService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: TelemetryAgent
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: aws.greengrass.Cli
    Version: 2.5.6
    State: RUNNING
    Configuration: {"AuthorizedPosixGroups":null,"AuthorizedWindowsGroups":null}
```    
                        
### To deploy the Greengrass CLI component (AWS CLI)

arn:aws:iot:ap-northeast-2:account-id:thing/GreengrassCore

![noname](https://user-images.githubusercontent.com/52392004/173241708-ad053a77-3079-4d45-b9fc-afb1ca740b8d.png)


arn:aws:iot:ap-northeast-2:account-id:thinggroup/GreengrassGroup

![noname](https://user-images.githubusercontent.com/52392004/173241860-a045202c-de5a-4a13-a8ec-12bec2060be0.png)



