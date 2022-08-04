# Lambda Component

## Lambda 생성 

#### AWS Lambda mappings

- One Lambda to one component
- Refactor single AWS Lambda functions to multiple, dependent components

#### Import AWS Lambda functions to components

```c
aws greengrassv2 create-component-version --lambda-arn 
```

#### Map subscriptions to component via authorization templates



## Hello World

[Tutorial creating hello world greengrass Lambda (in Python)](https://www.youtube.com/watch?v=jvQsygmzov0)을 참조하여 Hello World component를 생성하여 봅니다. 

1) [hello-world-python](https://github.com/aws-samples/aws-greengrass-samples/blob/master/hello-world-python/greengrassHelloWorld.py)을 다운로드 합니다. 





## Reference


[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)


[Tutorial creating hello world greengrass Lambda (in Python)](https://www.youtube.com/watch?v=jvQsygmzov0)

[Tutorial for a Greengrass Lambda listening to an MQTT Topic](https://www.youtube.com/watch?v=z9ju6FJ3Xlo)

[rpi-greengrass](https://github.com/miman/rpi-greengrass/blob/master/hello-world/README.md)

[2020 Greengrass Demo | Person recognition & counting project using AWS Lambda](https://www.youtube.com/watch?v=bRWT_sbzGds)

[PersonCountingRaspberry on the Edge using AWS Greengrass](https://github.com/Rauchdimehdi/PersonCountingRaspberry)

[Install the AWS IoT Device SDK for Python](https://docs.aws.amazon.com/greengrass/v1/developerguide/IoT-SDK.html)
