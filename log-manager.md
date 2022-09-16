# Log Manager

Log manager component (aws.greengrass.LogManager)는 Greengress core device의 로그를 업로드하여 CloudWatch에서 조회 할수 있도록 해줍니다. 이때 전달할 수 있는 로그에는 nucleus와 Component에 대한 로그뿐 아니라, greengrass 이외의 다른 application과 service의 로그까지 전송 가능합니다. 

[Necleus와 component에서 생성하는 Log](https://docs.aws.amazon.com/greengrass/v2/developerguide/monitor-logs.html#access-local-logs)는 매시간 또는 로그 크기가 일정크기(default: 1024KB)보다 커지면 다른 이름으로 저장하는데, 이때 log manager가 변경된 파일을 확인하여, 일정시간(기본값: 5분)마다 로그를 업로드 할 수 있습니다. 

## Required Policy

```java
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogStreams"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

## Endpoints 와 ports

component의 요청에 대한 Endpoint와 Port는 아래와 같습니다.

![image](https://user-images.githubusercontent.com/52392004/190610525-15e5710f-8f6f-4cad-9f9f-c36a1173fc71.png)

## Example: Configuration merge update

아래와 같은 configuration 적용시에 system logs와 com.example.HelloWorld component logs들을 CloudWatch Logs로 전송할 수 있습니다.

```java
{
  "logsUploaderConfiguration": {
    "systemLogsConfiguration": {
      "uploadToCloudWatch": "true",
      "minimumLogLevel": "INFO",
      "diskSpaceLimit": "10",
      "diskSpaceLimitUnit": "MB",
      "deleteLogFileAfterCloudUpload": "false"
    },
    "componentLogsConfigurationMap": {
      "com.example.HelloWorld": {
        "minimumLogLevel": "INFO",
        "diskSpaceLimit": "20",
        "diskSpaceLimitUnit": "MB",
        "deleteLogFileAfterCloudUpload": "false"
      }
    }
  },
  "periodicUploadIntervalSec": "300"
}
```


## Reference

[Log manager](https://docs.aws.amazon.com/greengrass/v2/developerguide/log-manager-component.html)

[Monitor AWS IoT Greengrass logs](https://docs.aws.amazon.com/greengrass/v2/developerguide/monitor-logs.html#access-local-logs)

