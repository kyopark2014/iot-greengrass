# AWS IoT Greengrass

## EC2에 Greengrass 설치

[EC2에 Greengrass 설치하기](https://github.com/kyopark2014/iot-greengrass/blob/main/ec2-greengrass.md)에 따라서 Greengrass를 설치합니다. 


## Workshop

[AWS IoT Greengrass V2 for beginners (Korean)](https://catalog.us-east-1.prod.workshops.aws/workshops/0b21ceb7-2108-4a82-9e76-4c56d4b52db5/ko-KR)의 워크샵을 수행합니다. 


arn:aws:iot:ap-northeast-2:account-id:thing/GreengrassCore

![noname](https://user-images.githubusercontent.com/52392004/173241708-ad053a77-3079-4d45-b9fc-afb1ca740b8d.png)


arn:aws:iot:ap-northeast-2:account-id:thinggroup/GreengrassGroup

![noname](https://user-images.githubusercontent.com/52392004/173241860-a045202c-de5a-4a13-a8ec-12bec2060be0.png)



[Deploy the Greengrass CLI component](https://docs.aws.amazon.com/greengrass/v2/developerguide/install-gg-cli.html)을 따라 아래와 같이 Greengrass cli를 설치합니다. 


1) [AWS IoT Console] - [Greengrass devices] - [Component]로 진입하여 "Public compenents"중에 "aws.greengrass.Cli"을 선택합니다.  

https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/components/public

2) [aws.greengrass.Cli]에서 아래처럼 "Deploy"를 선택하여 

![noname](https://user-images.githubusercontent.com/52392004/173242333-d07efb54-4821-4bbc-8a40-4a8595d7f3d1.png)

3) [Create new deployment]를 선택합니다.

![noname](https://user-images.githubusercontent.com/52392004/173242582-188ccb81-cd32-4c91-b72e-56d97c388a0b.png)

4) [Specify target]에서 [Target type]으로 "Thing group"을 선택하고, [Target name]으로 생성한 group 이름을 선택합니다. 여기서는 기 생성한 "GreengrassGroup"을 선택합니다. 이후 [Next]를 선택합니다. 

5) 이후 [Select components]에 "aws.greengrass.Cli"가 선택되었는지 확인 후, [Next]를 선택합니다. 

6) [Configure components]에서 Selected components에 "aws.greengrass.Cli" 확인후 [Next]를 선택합니다. 

7) [Configure advanced settings - optional에서도 마찬가지로 [Next]를 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/173242931-885f4d90-bc64-4251-af93-51b4904b28f3.png)

8) [Review]후에 [Deploy]를 선택합니다.  
