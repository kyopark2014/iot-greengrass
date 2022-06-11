# EC2에 greengrass 설치하기

## EC2 user 만들기

## greengrass 설치 

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

```c
$ sudo yum install java-1.8.0-openjdk
```

3) install

```c
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar \
--aws-region ap-northeast-2 \
--thing-name GreengrassCore \
--thing-group-name GreengrassGroup \
--component-default-user ggc_user:ggc_group \
--provision true \
--setup-system-service true \
--deploy-dev-tools true
```



## Troubleshooting

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

## config 확인

```c
echo $AWS_DEFAULT_REGION
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
echo $AWS_SESSION_TOKEN
```

아래처럼 입력합니다. 

```c
export AWS_DEFAULT_REGION=ap-northeast-2
export AWS_ACCESS_KEY_ID=SAMPLEIXN5TFSRWUTG2
export AWS_SECRET_ACCESS_KEY=SAMPLE2mOX9sDr9UxE6GELyT9Xkhc6a5nPFDcgc
```
