# Greengrass를 위한 계정 등록 

IAM console에서 Create Policy를 선택하여 "aws-policy-greengrass"를 생성합니다. 

https://us-east-1.console.aws.amazon.com/iamv2/home#/policies

이때 입력하는 policy는 [Minimal IAM policy for installer to provision resources](https://docs.aws.amazon.com/greengrass/v2/developerguide/provision-minimal-iam-policy.html)을 참조하여 아래처럼 생성합니다. 

```java
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CreateTokenExchangeRole",
            "Effect": "Allow",
            "Action": [
                "iam:AttachRolePolicy",
                "iam:CreatePolicy",
                "iam:CreateRole",
                "iam:GetPolicy",
                "iam:GetRole",
                "iam:PassRole"
            ],
            "Resource": [
                "arn:aws:iam::account-id:role/GreengrassV2TokenExchangeRole",
                "arn:aws:iam::account-id:policy/GreengrassV2TokenExchangeRoleAccess"
            ]
        },
        {
            "Sid": "CreateIoTResources",
            "Effect": "Allow",
            "Action": [
                "iot:AddThingToThingGroup",
                "iot:AttachPolicy",
                "iot:AttachThingPrincipal",
                "iot:CreateKeysAndCertificate",
                "iot:CreatePolicy",
                "iot:CreateRoleAlias",
                "iot:CreateThing",
                "iot:CreateThingGroup",
                "iot:DescribeEndpoint",
                "iot:DescribeRoleAlias",
                "iot:DescribeThingGroup",
                "iot:GetPolicy"
            ],
            "Resource": "*"
        },
        {
            "Sid": "DeployDevTools",
            "Effect": "Allow",
            "Action": [
                "greengrass:CreateDeployment",
                "iot:CancelJob",
                "iot:CreateJob",
                "iot:DeleteThingShadow",
                "iot:DescribeJob",
                "iot:DescribeThing",
                "iot:DescribeThingGroup",
                "iot:GetThingShadow",
                "iot:UpdateJob",
                "iot:UpdateThingShadow"
            ],
            "Resource": "*"
        }
    ]
}
```

[IAM console]에서 [Add user]를 선택하여, "iotuser"로 계정을 생성합니다.

https://us-east-1.console.aws.amazon.com/iamv2/home#/users

이때 "Add permissions"을 선택하여 아래와 같은 퍼미션을 추가합니다. 

![image](https://user-images.githubusercontent.com/52392004/173210257-c10dc32e-f7db-4e55-b7e3-b3a3cc327b61.png)

