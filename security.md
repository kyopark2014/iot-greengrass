# Security

## Greengrass와 IoT Core 구간의 Security

IoT의 데이터를 안전하게 모으고 제어하기 위하여 VPN 또는 Direct Connect를 사용할 수 있습니다. 하지만, 여러가지 이유로 Public Network에 연결되었다면, IoT Core와 Device간 상호 TLS 인증서를 통해 기본적으로 보호가 됩니다. 추가적으로 방화벽 설정을 통해 특정 IP만 허용하는 방법이 있을수 있는데, IoT Core의 Endpoint는 동적 IP를 사용하므로 정적 IP를 부여할 수 없습니다. 따라서 아래와 같이 고정 IP를 사용하는 Endpoint를 만들어서 VPC endpoint로 IoT Core와 연결하면 동일한 동작을 구현 할 수 있습니다.

<img src="https://user-images.githubusercontent.com/52392004/184057209-2ccb4db5-85dd-4bac-b9df-97c4c0186651.png" width="800">

상세한 동작은 [Creating static IP addresses and custom domains for AWS IoT Core endpoints](https://aws.amazon.com/ko/blogs/iot/creating-static-ip-addresses-and-custom-domains-for-aws-iot-core-endpoints/)를 참조하고 [CDK 코드](https://github.com/aws-samples/aws-iot-endpoint-with-static-ips/blob/main/cdk/index.ts)를 통해 상세 동작을 확인 할 수 있습니다. 

추가적으로 [Getting Static IP for AWS IoT Core](https://anubhavjhalani.medium.com/getting-static-ip-for-aws-iot-core-64bc7a923fd5)에서는 Global Accelerator를 이용하는 방법도 설명하고 있습니다. 


## Nucleus security

#### RunAs ggc_user or privileged account (root)

Component들은 Nucleus 또는 OS에 등록된 user에 의해 실행됩니다. 

만약 향상된 privileges를 사용해야 할경우에는 RequiresPrivilege을 true로 설정합니다. 

#### Vended credentials via environment variables

AWS_REGION
SVCUID
AWS_CONTAINER_AUTHORIZATION_TOKEN
AWS_CONTAINER_CREDENTIALS_FULL_URI

## Authorization policies for IPC

```java
ComponentName: com.example.HelloWorld
ComponentConfiguration:
  DefaultConfiguration:
    accessControl:
      aws.greengrass.ipc.pubsub:
        com.example.HelloWorld:pubsub:1:
          policyDescription: Publish only single topic
          operations:
            - 'aws.greengrass#PublishToTopic'
          resources:
            - 'test/topicAAA'
        com.example.HelloWorld:pubsub:2:
          policyDescription: Publish AND subscribe to test/topic2
          operations:
            - 'aws.greengrass#PublishToTopic'
            - 'aws.greengrass#SubscribeToTopic'
          resources:
            - 'test/topicBBB'
```

## Reference 

[Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)


[Creating static IP addresses and custom domains for AWS IoT Core endpoints](https://aws.amazon.com/ko/blogs/iot/creating-static-ip-addresses-and-custom-domains-for-aws-iot-core-endpoints/)

              
