# Log Manager

Log manager의 component (aws.greengrass.LogManager)는 Greengress core device의 로그를 업로드하여 CloudWatch에서 조회 할수 있도록 해줍니다. 이때 전달할 수 있는 로그에는 nucleus와 Component에 대한 로그뿐 아니라 다른 application과 

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



## Reference

[Log manager](https://docs.aws.amazon.com/greengrass/v2/developerguide/log-manager-component.html)
