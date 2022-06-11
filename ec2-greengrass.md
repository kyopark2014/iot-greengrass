# EC2에 greengrass 설치하기

## EC2 user 만들기

## greengrass 설치 

1) 설치 파일을 다운로드 합니다. 

```c
$ curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip && unzip greengrass-nucleus-latest.zip -d GreengrassCore
Archive:  greengrass-nucleus-latest.zip
  inflating: GreengrassCore/LICENSE
  inflating: GreengrassCore/NOTICE
  inflating: GreengrassCore/README.md
  inflating: GreengrassCore/THIRD-PARTY-LICENSES
  inflating: GreengrassCore/bin/greengrass.exe
  inflating: GreengrassCore/bin/greengrass.service.template
  inflating: GreengrassCore/bin/greengrass.xml.template
  inflating: GreengrassCore/bin/loader
  inflating: GreengrassCore/bin/loader.cmd
  inflating: GreengrassCore/conf/recipe.yaml
  inflating: GreengrassCore/lib/Greengrass.jar
```  

2) java 설치하기 

