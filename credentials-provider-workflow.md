# Credentials Provider Workflow

AWS IoT Core credential provider 기능 사용을 위해서 IAM Role을 설정하여야 합니다. 이를 통해 디바이스 인증서를 이용하여 보안 토큰을 발급할 수 있는데, 이 토큰으로 Core device는 AWS 서비스 접근 권한을 획득 할 수 있습니다. 

## IAM role: GreengrassV2TokenExchangeRole

This role has a policy named GreengrassV2TokenExchangeRoleAccess and a trust relationship that allows credentials.iot.amazonaws.com to assume the role. The policy includes the minimum permissions for the core device.

This policy doesn't include access to files in S3 buckets. You must add permissions to the role to allow core devices to retrieve component artifacts from S3 buckets. For more information, see Allow access to S3 buckets for component artifacts.

AWS IoT role alias: GreengrassV2TokenExchangeRoleAlias
This role alias refers to the IAM role.

GreengrassV2TokenExchangeRoleAccess에 대한 policy는 아래와 같습니다. 

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

아래와 같이 S3에 대한 권한을 설정할 수 있습니다. 단, 상용시에서는 Resouces는 해당 bucket이름으로 제한하여야 합니다. 

```java
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::*"
        }
    ]
}
```

참고로 이것에 대한 trusted entries는 아래와 같습니다. 

```java
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "credentials.iot.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
``` 

## Credentials provider workflow

![image](https://user-images.githubusercontent.com/52392004/181392716-4b78f2f8-202a-4190-a8e0-69a9fbd6b5ea.png)

1. The AWS IoT Core device makes an HTTPS request to the credentials provider for a security token. The request includes the device X.509 certificate for authentication.

2. The credentials provider forwards the request to the AWS IoT Core authentication and authorization module to validate the certificate and verify that the device has permission to request the security token.

3. If the certificate is valid and has permission to request a security token, the AWS IoT Core authentication and authorization module returns success. Otherwise, it sends an exception to the device.

4. After successfully validating the certificate, the credentials provider invokes the AWS Security Token Service (AWS STS) to assume the IAM role that you created for it.

5. AWS STS returns a temporary, limited-privilege security token to the credentials provider.

6. The credentials provider returns the security token to the device.

7. The device uses the security token to sign an AWS request with AWS Signature Version 4.

8. The requested service invokes IAM to validate the signature and authorize the request against access policies attached to the IAM role that you created for the credentials provider.

9. If IAM validates the signature successfully and authorizes the request, the request is successful. Otherwise, IAM sends an exception.



## Credentials provider endpoint 

```c
aws iot describe-endpoint --endpoint-type iot:CredentialProvider
{
    "endpointAddress": "samplekbg1m4dh.credentials.iot.ap-northeast-2.amazonaws.com"
}
```


## Reference

[Credentials Provider Workflow](https://docs.aws.amazon.com/iot/latest/developerguide/authorizing-direct-aws.html)
