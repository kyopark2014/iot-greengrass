## Amazon S3을 이용한 Greengrass device 배포환경 구축하기 

아래의 Policy를 가지는 "GGv2WorkshopS3Policy"을 생성합니다. 

```java
	 {
            "Sid": "DeployDevTools",
            "Effect": "Allow",
            "Action": [
                "greengrass:CreateDeployment",
                "greengrass:GetServiceRoleForAccount",
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
```

"GGv2WorkshopS3Policy" Policy를 "GreengrassV2TokenExchangeRole"에 추가합니다.

