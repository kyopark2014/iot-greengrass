## Greengrass device의 GreengrassV2TokenExchangeRole에 Amazon S3 Role 추가

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

