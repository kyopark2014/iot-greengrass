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

1) "example-lambda-python" 폴더를 생성합니다.

2) [hello-world-python](https://github.com/aws-samples/aws-greengrass-samples/blob/master/hello-world-python/greengrassHelloWorld.py)을 다운로드 합니다. 

3) greengrasssdk를 다운로드합니다.

```c
git clone https://github.com/aws/aws-greengrass-core-sdk-python 
```

4) "example-lambda-python"에 greengrasssdk를 아래처럼 복사를 합니다. 

```c
cp -R aws-greengrass-core-sdk-python/greengrasssdk example-lambda-python/
```

5) lambda 함수에 업로드하기 위하여 압축을 합니다. 

```c
cd example-lambda-python
zip -r deploy.zip *
```

6) [[AWS Lambda] - [Functions]](https://ap-northeast-2.console.aws.amazon.com/lambda/home?region=ap-northeast-2#/functions)에서 [Create function]을 선택하고, [function name]에 "example-lambda-python"을 입력하고 [Runtime]으로 적절한 Python 라이브러리를 선택한 후에 [Create function]을 선택합니다. 

7) 상단 오른쪽의 [Upload from]에서 [.zip]을 선택한 후에 "deploy.zip"을 선택하여 업로드 합니다. 




## Reference



[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)


[Tutorial creating hello world greengrass Lambda (in Python)](https://www.youtube.com/watch?v=jvQsygmzov0)

[Tutorial for a Greengrass Lambda listening to an MQTT Topic](https://www.youtube.com/watch?v=z9ju6FJ3Xlo)

[rpi-greengrass](https://github.com/miman/rpi-greengrass/blob/master/hello-world/README.md)

[2020 Greengrass Demo | Person recognition & counting project using AWS Lambda](https://www.youtube.com/watch?v=bRWT_sbzGds)

[PersonCountingRaspberry on the Edge using AWS Greengrass](https://github.com/Rauchdimehdi/PersonCountingRaspberry)
