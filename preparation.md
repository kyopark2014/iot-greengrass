# Greengrass Preperation

### Greengrass installation 

[Workshop Greengrass](https://github.com/kyopark2014/iot-greengrass/blob/main/workshop-greengrass-beginner.md)을 참조하여 아래와 같이 Greengrass를 설치할 수 있습니다. 

1) Greengrass 다운로드합니다. 

```java
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip 
unzip greengrass-nucleus-latest.zip -d GreengrassCore
```

2)  IoT Core에 thing을 생성하고, greengrass에 등록합니다. thing-nam과 thing-group-name 용도에 맞게 설정하여야 합니다. 

```java
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar \
	--aws-region ap-northeast-2 \
	--thing-name GreengrassCore-18163f7ac3e \
	--thing-group-name GreengrassGroup \
	--component-default-user ggc_user:ggc_group \
	--provision true \
	--setup-system-service true \
	--deploy-dev-tools true
```
