# EC2에 Greengrass 설치하기

## EC2 user 만들기

1) IoT용 계정 만들기 

[Greengrass를 위한 계정 등록](https://github.com/kyopark2014/iot-greengrass/blob/main/greengrass-user-registration.md)에 따라 IoT용 계정이 미리 생성되어 있어야 합니다. 

2) EC2 생성 및 접속

EC2 console에 접속하여 [Launch instances]를 선택하여 "GreenGrass"라는 이름으로 EC2를 생성합니다. 이때, OS는 "Amazon Linux", Instance type은 "t2.micro"를 선택하였습니다. 

https://ap-northeast-2.console.aws.amazon.com/ec2/v2/home?region=ap-northeast-2#Instances:v=3

ssh를 이용해 아래처럼 접속합니다. 여기서 EC2의 ip는 "Public IPv4 address"에 있는 ipv4 address를 사용합니다. 

```c
$ ssh ec2-user@150.223.112.443 -i ssh-seoul.cer
```


## Greengrass 설치 

1) 설치 파일을 다운로드 합니다. 

```c
$ curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip && unzip greengrass-nucleus-latest.zip -d GreengrassCore
Archive:  greengrass-nucleus-latest.zip
  inflating: GreengrassCore/LICENSE
  inflating: GreengrassCore/NOTICE
  inflating: GreengrassCore/README.md
  inflating: GreengrassCore/THIRD-PARTY-LICENSES
  inflating: GreengrassCore/bin/greengrass.exe
  inflating: GreengrassCore/bin/greengrass.service.template
  inflating: GreengrassCore/bin/greengrass.xml.template
  inflating: GreengrassCore/bin/loader
  inflating: GreengrassCore/bin/loader.cmd
  inflating: GreengrassCore/conf/recipe.yaml
  inflating: GreengrassCore/lib/Greengrass.jar
```  

2) java 설치하기 

아래와 같이 java를 설치하여 줍니다.

```c
$ sudo yum install java-1.8.0-openjdk
```

3) config 확인

아래와 같이 config 확인 명령어를 통해 변수들이 export 되어 있는지 확인 합니다. 

```c
echo $AWS_DEFAULT_REGION
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
```

변수값 확인후 입력이 필요한 경우에 아래처럼 입력합니다. 

```c
export AWS_DEFAULT_REGION=ap-northeast-2
export AWS_ACCESS_KEY_ID=SAMPLSample5TI2W4DP4B
export AWS_SECRET_ACCESS_KEY=SamPle+ulrFsfsY0+gWeU3Sample5W4E2zuaZpc
```

3) 아래와 같이 greengrass installer를 실행해줍니다.

여기서 things name을 GreengrassCore로, thing group 이름을 GreengrassGroup을 지정했습니다. 특히, things 이름이 중복되지 않도록 넣어주어야 합니다. [Installer arguments](https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-installer.html)에서 각 argument에 대한 상세한 내용을 알 수 있습니다. 

```c
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar \
--aws-region ap-northeast-2 \
--thing-name GreengrassCore \
--thing-group-name GreengrassGroup \
--component-default-user ggc_user:ggc_group \
--provision true \
--setup-system-service true \
--deploy-dev-tools true

Provisioning AWS IoT resources for the device with IoT Thing Name: [GreengrassCore]...
Found IoT policy "GreengrassV2IoTThingPolicy", reusing it
Creating keys and certificate...
Attaching policy to certificate...
Creating IoT Thing "GreengrassCore"...
Attaching certificate to IoT thing...
Successfully provisioned AWS IoT resources for the device with IoT Thing Name: [GreengrassCore]!
Adding IoT Thing [GreengrassCore] into Thing Group: [GreengrassGroup]...
IoT Thing Group "GreengrassGroup" already existed, reusing it
Successfully added Thing into Thing Group: [GreengrassGroup]
Setting up resources for aws.greengrass.TokenExchangeService ...
TES role alias "GreengrassV2TokenExchangeRoleAlias" does not exist, creating new alias...
TES role "GreengrassV2TokenExchangeRole" does not exist, creating role...
IoT role policy "GreengrassTESCertificatePolicyGreengrassV2TokenExchangeRoleAlias" for TES Role alias not exist, creating policy...
Attaching TES role policy to IoT thing...
Encountered error - User: arn:aws:iam::677146750822:user/iotuser is not authorized to perform: iam:GetPolicy on resource: policy arn:aws:iam::aws:policy/GreengrassV2TokenExchangeRoleAccess because no identity-based policy allows the iam:GetPolicy action (Service: Iam, Status Code: 403, Request ID: 540fb048-39d5-4881-93d5-a93e91ef9223, Extended Request ID: null); No permissions to lookup managed policy, looking for a user defined policy...
No IAM policy found, will attempt creating one...
IAM role policy for TES "GreengrassV2TokenExchangeRoleAccess" created. This policy DOES NOT have S3 access, please modify it with your private components' artifact buckets/objects as needed when you create and deploy private components
Attaching IAM role policy for TES to IAM role for TES...
Configuring Nucleus with provisioned resource details...
Downloading Root CA from "https://www.amazontrust.com/repository/AmazonRootCA1.pem"
Created device configuration
Successfully configured Nucleus with provisioned resource details!
Thing group exists, it could have existing deployment and devices, hence NOT creating deployment for Greengrass first party dev tools, please manually create a deployment if you wish to
Creating user ggc_user
ggc_user created
Creating group ggc_group
ggc_group created
Added ggc_user to ggc_group
Successfully set up Nucleus as a system service
```





## Troubleshooting

### Unable to load credentials
아래와 같이 설치시 "unable to load credentials"에러가 발생시, [config 확인]을 참조하여 credential을 export 합니다. 

```c
$ sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar --aws-region ap-northeast-2 --thing-name GreengrassCore --thing-group-name GreengrassGroup --component-default-user ggc_user:ggc_group --provision true --setup-system-service true --deploy-dev-tools true
Provisioning AWS IoT resources for the device with IoT Thing Name: [GreengrassCore]...
Error while trying to setup Greengrass Nucleus
software.amazon.awssdk.core.exception.SdkClientException: Unable to load credentials from any of the providers in the chain AwsCredentialsProviderChain(credentialsProviders=[SystemPropertyCredentialsProvider(), EnvironmentVariableCredentialsProvider(), WebIdentityTokenCredentialsProvider(), ProfileCredentialsProvider(), ContainerCredentialsProvider(), InstanceProfileCredentialsProvider()]) : [SystemPropertyCredentialsProvider(): Unable to load credentials from system settings. Access key must be specified either via environment variable (AWS_ACCESS_KEY_ID) or system property (aws.accessKeyId)., EnvironmentVariableCredentialsProvider(): Unable to load credentials from system settings. Access key must be specified either via environment variable (AWS_ACCESS_KEY_ID) or system property (aws.accessKeyId)., WebIdentityTokenCredentialsProvider(): Either the environment variable AWS_WEB_IDENTITY_TOKEN_FILE or the javaproperty aws.webIdentityTokenFile must be set., ProfileCredentialsProvider(): Profile file contained no credentials for profile 'default': ProfileFile(profiles=[]), ContainerCredentialsProvider(): Cannot fetch credentials from container - neither AWS_CONTAINER_CREDENTIALS_FULL_URI or AWS_CONTAINER_CREDENTIALS_RELATIVE_URI environment variables are set., InstanceProfileCredentialsProvider(): The requested metadata is not found at http://169.254.169.254/latest/meta-data/iam/security-credentials/]
	at software.amazon.awssdk.core.exception.SdkClientException$BuilderImpl.build(SdkClientException.java:98)
	at software.amazon.awssdk.auth.credentials.AwsCredentialsProviderChain.resolveCredentials(AwsCredentialsProviderChain.java:112)
	at software.amazon.awssdk.auth.credentials.internal.LazyAwsCredentialsProvider.resolveCredentials(LazyAwsCredentialsProvider.java:45)
	at software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider.resolveCredentials(DefaultCredentialsProvider.java:105)
	at software.amazon.awssdk.awscore.internal.AwsExecutionContextBuilder.resolveCredentials(AwsExecutionContextBuilder.java:171)
	at software.amazon.awssdk.awscore.internal.AwsExecutionContextBuilder.invokeInterceptorsAndCreateExecutionContext(AwsExecutionContextBuilder.java:108)
	at software.amazon.awssdk.awscore.client.handler.AwsSyncClientHandler.invokeInterceptorsAndCreateExecutionContext(AwsSyncClientHandler.java:69)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.lambda$execute$1(BaseSyncClientHandler.java:78)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.measureApiCallSuccess(BaseSyncClientHandler.java:175)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.execute(BaseSyncClientHandler.java:76)
	at software.amazon.awssdk.core.client.handler.SdkSyncClientHandler.execute(SdkSyncClientHandler.java:45)
	at software.amazon.awssdk.awscore.client.handler.AwsSyncClientHandler.execute(AwsSyncClientHandler.java:56)
	at software.amazon.awssdk.services.iot.DefaultIotClient.getPolicy(DefaultIotClient.java:8787)
	at com.aws.greengrass.easysetup.DeviceProvisioningHelper.createThing(DeviceProvisioningHelper.java:204)
	at com.aws.greengrass.easysetup.GreengrassSetup.provision(GreengrassSetup.java:508)
	at com.aws.greengrass.easysetup.GreengrassSetup.performSetup(GreengrassSetup.java:319)
	at com.aws.greengrass.easysetup.GreengrassSetup.main(GreengrassSetup.java:269)
```  


### no identity-based policy allows the iam:GetRole action

아래와 같이 "no identity-based policy allows the iam:GetRole action" 에러가 발생하는 경우에, [Minimal IAM policy for installer to provision resources](https://docs.aws.amazon.com/greengrass/v2/developerguide/provision-minimal-iam-policy.html)에 따라 policy가 추가 되어 있는지 확인 합니다. 

```c
$ sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar --aws-region ap-northeast-2 --thing-name GreengrassCore --thing-group-name GreengrassGroup --component-default-user ggc_user:ggc_group --provision true --setup-system-service true --deploy-dev-tools true
Provisioning AWS IoT resources for the device with IoT Thing Name: [GreengrassCore]...
Found IoT policy "GreengrassV2IoTThingPolicy", reusing it
Creating keys and certificate...
Attaching policy to certificate...
Creating IoT Thing "GreengrassCore"...
Attaching certificate to IoT thing...
Successfully provisioned AWS IoT resources for the device with IoT Thing Name: [GreengrassCore]!
Adding IoT Thing [GreengrassCore] into Thing Group: [GreengrassGroup]...
IoT Thing Group "GreengrassGroup" already existed, reusing it
Successfully added Thing into Thing Group: [GreengrassGroup]
Setting up resources for aws.greengrass.TokenExchangeService ...
TES role alias "GreengrassV2TokenExchangeRoleAlias" does not exist, creating new alias...
Error while trying to setup Greengrass Nucleus
software.amazon.awssdk.services.iam.model.IamException: User: arn:aws:iam::account-id:user/iotuser is not authorized to perform: iam:GetRole on resource: role GreengrassV2TokenExchangeRole because no identity-based policy allows the iam:GetRole action (Service: Iam, Status Code: 403, Request ID: b2172499-7064-4650-9f70-24117c83b836, Extended Request ID: null)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handleErrorResponse(CombinedResponseHandler.java:123)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handleResponse(CombinedResponseHandler.java:79)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handle(CombinedResponseHandler.java:59)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handle(CombinedResponseHandler.java:40)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.HandleResponseStage.execute(HandleResponseStage.java:40)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.HandleResponseStage.execute(HandleResponseStage.java:30)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptTimeoutTrackingStage.execute(ApiCallAttemptTimeoutTrackingStage.java:73)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptTimeoutTrackingStage.execute(ApiCallAttemptTimeoutTrackingStage.java:42)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.TimeoutExceptionHandlingStage.execute(TimeoutExceptionHandlingStage.java:78)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.TimeoutExceptionHandlingStage.execute(TimeoutExceptionHandlingStage.java:40)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptMetricCollectionStage.execute(ApiCallAttemptMetricCollectionStage.java:50)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptMetricCollectionStage.execute(ApiCallAttemptMetricCollectionStage.java:36)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.RetryableStage.execute(RetryableStage.java:81)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.RetryableStage.execute(RetryableStage.java:36)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.StreamManagingStage.execute(StreamManagingStage.java:56)
	at software.amazon.awssdk.core.internal.http.StreamManagingStage.execute(StreamManagingStage.java:36)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallTimeoutTrackingStage.executeWithTimer(ApiCallTimeoutTrackingStage.java:80)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallTimeoutTrackingStage.execute(ApiCallTimeoutTrackingStage.java:60)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallTimeoutTrackingStage.execute(ApiCallTimeoutTrackingStage.java:42)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallMetricCollectionStage.execute(ApiCallMetricCollectionStage.java:48)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallMetricCollectionStage.execute(ApiCallMetricCollectionStage.java:31)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ExecutionFailureExceptionReportingStage.execute(ExecutionFailureExceptionReportingStage.java:37)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ExecutionFailureExceptionReportingStage.execute(ExecutionFailureExceptionReportingStage.java:26)
	at software.amazon.awssdk.core.internal.http.AmazonSyncHttpClient$RequestExecutionBuilderImpl.execute(AmazonSyncHttpClient.java:193)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.invoke(BaseSyncClientHandler.java:103)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.doExecute(BaseSyncClientHandler.java:167)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.lambda$execute$1(BaseSyncClientHandler.java:82)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.measureApiCallSuccess(BaseSyncClientHandler.java:175)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.execute(BaseSyncClientHandler.java:76)
	at software.amazon.awssdk.core.client.handler.SdkSyncClientHandler.execute(SdkSyncClientHandler.java:45)
	at software.amazon.awssdk.awscore.client.handler.AwsSyncClientHandler.execute(AwsSyncClientHandler.java:56)
	at software.amazon.awssdk.services.iam.DefaultIamClient.getRole(DefaultIamClient.java:5370)
	at com.aws.greengrass.easysetup.DeviceProvisioningHelper.setupIoTRoleForTes(DeviceProvisioningHelper.java:400)
	at com.aws.greengrass.easysetup.GreengrassSetup.provision(GreengrassSetup.java:519)
	at com.aws.greengrass.easysetup.GreengrassSetup.performSetup(GreengrassSetup.java:319)
	at com.aws.greengrass.easysetup.GreengrassSetup.main(GreengrassSetup.java:269)
```

### not authorized to perform: iot:GetPolicy

[config 확인]을 참조하여 credential을 export 합니다. 

```c
$ sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar --aws-region ap-northeast-2 --thing-name GreengrassCore --thing-group-name GreengrassGroup --component-default-user ggc_user:ggc_group --provision true --setup-system-service true --deploy-dev-tools true
Provisioning AWS IoT resources for the device with IoT Thing Name: [GreengrassCore]...
Error while trying to setup Greengrass Nucleus
software.amazon.awssdk.services.iot.model.IotException: User: arn:aws:sts::account-id:assumed-role/SSMDefaultRoleForPVREReporting/i-00c1d0d9a41d5c661 is not authorized to perform: iot:GetPolicy on resource: arn:aws:iot:ap-northeast-2:account-id:policy/GreengrassV2IoTThingPolicy because no identity-based policy allows the iot:GetPolicy action (Service: Iot, Status Code: 403, Request ID: b98e19c2-cf59-4333-9c06-78453ce1ce7a, Extended Request ID: null)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handleErrorResponse(CombinedResponseHandler.java:123)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handleResponse(CombinedResponseHandler.java:79)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handle(CombinedResponseHandler.java:59)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handle(CombinedResponseHandler.java:40)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.HandleResponseStage.execute(HandleResponseStage.java:40)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.HandleResponseStage.execute(HandleResponseStage.java:30)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptTimeoutTrackingStage.execute(ApiCallAttemptTimeoutTrackingStage.java:73)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptTimeoutTrackingStage.execute(ApiCallAttemptTimeoutTrackingStage.java:42)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.TimeoutExceptionHandlingStage.execute(TimeoutExceptionHandlingStage.java:78)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.TimeoutExceptionHandlingStage.execute(TimeoutExceptionHandlingStage.java:40)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptMetricCollectionStage.execute(ApiCallAttemptMetricCollectionStage.java:50)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptMetricCollectionStage.execute(ApiCallAttemptMetricCollectionStage.java:36)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.RetryableStage.execute(RetryableStage.java:81)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.RetryableStage.execute(RetryableStage.java:36)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.StreamManagingStage.execute(StreamManagingStage.java:56)
	at software.amazon.awssdk.core.internal.http.StreamManagingStage.execute(StreamManagingStage.java:36)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallTimeoutTrackingStage.executeWithTimer(ApiCallTimeoutTrackingStage.java:80)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallTimeoutTrackingStage.execute(ApiCallTimeoutTrackingStage.java:60)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallTimeoutTrackingStage.execute(ApiCallTimeoutTrackingStage.java:42)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallMetricCollectionStage.execute(ApiCallMetricCollectionStage.java:48)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallMetricCollectionStage.execute(ApiCallMetricCollectionStage.java:31)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ExecutionFailureExceptionReportingStage.execute(ExecutionFailureExceptionReportingStage.java:37)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ExecutionFailureExceptionReportingStage.execute(ExecutionFailureExceptionReportingStage.java:26)
	at software.amazon.awssdk.core.internal.http.AmazonSyncHttpClient$RequestExecutionBuilderImpl.execute(AmazonSyncHttpClient.java:193)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.invoke(BaseSyncClientHandler.java:103)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.doExecute(BaseSyncClientHandler.java:167)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.lambda$execute$1(BaseSyncClientHandler.java:82)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.measureApiCallSuccess(BaseSyncClientHandler.java:175)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.execute(BaseSyncClientHandler.java:76)
	at software.amazon.awssdk.core.client.handler.SdkSyncClientHandler.execute(SdkSyncClientHandler.java:45)
	at software.amazon.awssdk.awscore.client.handler.AwsSyncClientHandler.execute(AwsSyncClientHandler.java:56)
	at software.amazon.awssdk.services.iot.DefaultIotClient.getPolicy(DefaultIotClient.java:8787)
	at com.aws.greengrass.easysetup.DeviceProvisioningHelper.createThing(DeviceProvisioningHelper.java:204)
	at com.aws.greengrass.easysetup.GreengrassSetup.provision(GreengrassSetup.java:508)
	at com.aws.greengrass.easysetup.GreengrassSetup.performSetup(GreengrassSetup.java:319)
	at com.aws.greengrass.easysetup.GreengrassSetup.main(GreengrassSetup.java:269)
```	

## The security token included in the request is invalid

credential을 확인 합니다. 

```c
$ sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar --aws-region ap-northeast-2 --thing-name GreengrassCore --thing-group-name GreengrassGroup --component-default-user ggc_user:ggc_group --provision true --setup-system-service true --deploy-dev-tools true
Provisioning AWS IoT resources for the device with IoT Thing Name: [GreengrassCore]...
Found IoT policy "GreengrassV2IoTThingPolicy", reusing it
Creating keys and certificate...
Attaching policy to certificate...
Creating IoT Thing "GreengrassCore"...
Attaching certificate to IoT thing...
Successfully provisioned AWS IoT resources for the device with IoT Thing Name: [GreengrassCore]!
Adding IoT Thing [GreengrassCore] into Thing Group: [GreengrassGroup]...
IoT Thing Group "GreengrassGroup" already existed, reusing it
Successfully added Thing into Thing Group: [GreengrassGroup]
Setting up resources for aws.greengrass.TokenExchangeService ...
TES role alias "GreengrassV2TokenExchangeRoleAlias" does not exist, creating new alias...
Error while trying to setup Greengrass Nucleus
software.amazon.awssdk.services.iam.model.IamException: The security token included in the request is invalid (Service: Iam, Status Code: 403, Request ID: 0049f056-90b6-485a-b5ab-b6d199c07876, Extended Request ID: null)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handleErrorResponse(CombinedResponseHandler.java:123)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handleResponse(CombinedResponseHandler.java:79)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handle(CombinedResponseHandler.java:59)
	at software.amazon.awssdk.core.internal.http.CombinedResponseHandler.handle(CombinedResponseHandler.java:40)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.HandleResponseStage.execute(HandleResponseStage.java:40)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.HandleResponseStage.execute(HandleResponseStage.java:30)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptTimeoutTrackingStage.execute(ApiCallAttemptTimeoutTrackingStage.java:73)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptTimeoutTrackingStage.execute(ApiCallAttemptTimeoutTrackingStage.java:42)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.TimeoutExceptionHandlingStage.execute(TimeoutExceptionHandlingStage.java:78)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.TimeoutExceptionHandlingStage.execute(TimeoutExceptionHandlingStage.java:40)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptMetricCollectionStage.execute(ApiCallAttemptMetricCollectionStage.java:50)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallAttemptMetricCollectionStage.execute(ApiCallAttemptMetricCollectionStage.java:36)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.RetryableStage.execute(RetryableStage.java:81)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.RetryableStage.execute(RetryableStage.java:36)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.StreamManagingStage.execute(StreamManagingStage.java:56)
	at software.amazon.awssdk.core.internal.http.StreamManagingStage.execute(StreamManagingStage.java:36)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallTimeoutTrackingStage.executeWithTimer(ApiCallTimeoutTrackingStage.java:80)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallTimeoutTrackingStage.execute(ApiCallTimeoutTrackingStage.java:60)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallTimeoutTrackingStage.execute(ApiCallTimeoutTrackingStage.java:42)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallMetricCollectionStage.execute(ApiCallMetricCollectionStage.java:48)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ApiCallMetricCollectionStage.execute(ApiCallMetricCollectionStage.java:31)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.pipeline.RequestPipelineBuilder$ComposingRequestPipelineStage.execute(RequestPipelineBuilder.java:206)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ExecutionFailureExceptionReportingStage.execute(ExecutionFailureExceptionReportingStage.java:37)
	at software.amazon.awssdk.core.internal.http.pipeline.stages.ExecutionFailureExceptionReportingStage.execute(ExecutionFailureExceptionReportingStage.java:26)
	at software.amazon.awssdk.core.internal.http.AmazonSyncHttpClient$RequestExecutionBuilderImpl.execute(AmazonSyncHttpClient.java:193)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.invoke(BaseSyncClientHandler.java:103)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.doExecute(BaseSyncClientHandler.java:167)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.lambda$execute$1(BaseSyncClientHandler.java:82)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.measureApiCallSuccess(BaseSyncClientHandler.java:175)
	at software.amazon.awssdk.core.internal.handler.BaseSyncClientHandler.execute(BaseSyncClientHandler.java:76)
	at software.amazon.awssdk.core.client.handler.SdkSyncClientHandler.execute(SdkSyncClientHandler.java:45)
	at software.amazon.awssdk.awscore.client.handler.AwsSyncClientHandler.execute(AwsSyncClientHandler.java:56)
	at software.amazon.awssdk.services.iam.DefaultIamClient.getRole(DefaultIamClient.java:5370)
	at com.aws.greengrass.easysetup.DeviceProvisioningHelper.setupIoTRoleForTes(DeviceProvisioningHelper.java:400)
	at com.aws.greengrass.easysetup.GreengrassSetup.provision(GreengrassSetup.java:519)
	at com.aws.greengrass.easysetup.GreengrassSetup.performSetup(GreengrassSetup.java:319)
	at com.aws.greengrass.easysetup.GreengrassSetup.main(GreengrassSetup.java:269)
```	
