# Docker Container를 이용한 Component 생성

아래와 같이 ECR(Elastic Container Registry), S3 또는 다른 Docker registry에서 이미지를 가져와서 Component를 생성할 수 있습니다. 

![image](https://user-images.githubusercontent.com/52392004/181383024-b5a23ef4-8b56-4d41-b4c9-6d7256c02081.png)

Greengrass V1.x에서는 Docker connector를 이용하였고 V2.0에서는 Component의 Recipe의 environment variable에 정의된 registry에서 Docker Component를 생성하게 됩니다. 

## Docker Container Preparation

Greengrass에서 Docker Container를 Component이용하기 위해서는 아래와 같은 설정이 필요합니다. 

Greengrass 디바이스에 접속하여 아래와 같이 사용자를 docker user group에 추가하여야 합니다. 

```java
sudo usermod -aG docker ggc_user
```

ECR을 사용하기 위해서는 [device role](https://docs.aws.amazon.com/greengrass/v2/developerguide/device-service-role.html)을 참조하여, [IAM Console](https://us-east-1.console.aws.amazon.com/iamv2/home?region=ap-northeast-2#/roles/details/GreengrassV2TokenExchangeRole?section=permissions)에서 GreengrassV2TokenExchangeRole에 아래의 permission을 추가합니다. 

```java
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ],
      "Resource": [
        "*"
      ],
      "Effect": "Allow"
    }
  ]
}
```


## Reference

[Workshop - AWS IoT Greengrass V2](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US)

