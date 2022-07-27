# Greeengrass 버전 차이점 

## V1.x

Deployment group을 이용하여 IoT Greengrass Connector들과 device들을 관리하고 Lambda를 사용할 수 있게 하는데, 아래와 같이 Greengrass Daemon(greengrassd)을 이용합니다. 이것은 OS에 맞추어 컴파일이 필요합니다. 

![image](https://user-images.githubusercontent.com/52392004/181127590-76ee28ba-3f67-4f17-a238-a03b2e47523d.png)


## V2.0

V1.x와 달리 Java를 사용하여 컴파일이 필요하지 않습니다. 이때 아래와 같이 Greengrass.jar 파일로 배포되고 JVM을 사용합니다. 또한, V2.0은 Component를 base로 동작하는데, Component는 Core(Greengrass.jar)나 IoT 제공자(provider)의 Nucleus, StreamManger, LogManager가 다르더라도 같은 구조를 가집니다. 

Component는 Descrete piece of code로서 Recipe file과 Artifacts로 구성됩니다. 여기에서는 AWS가 Public하게 제공하는 StreamManager과 Token exchange service와 같은것들이 있으며, 사용자가 정의한 Component는 등록후 사용가능합니다. 

![image](https://user-images.githubusercontent.com/52392004/181129681-435e1d24-c589-4fd0-ad93-947fbba34a05.png)


## Reference

[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)
