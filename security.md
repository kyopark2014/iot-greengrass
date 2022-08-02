# Security

## Nucleus security

#### RunAs ggc_user or privileged account (root)

Component들은 Necleus 또는 OS에 등록된 user에 의해 실행됩니다. 

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

              
