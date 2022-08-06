# Docker Container를 이용한 Component 생성

아래와 같이 ECR(Elastic Container Registry), S3 또는 다른 Docker registry에서 이미지를 가져와서 Component를 생성할 수 있습니다. 

![image](https://user-images.githubusercontent.com/52392004/181383024-b5a23ef4-8b56-4d41-b4c9-6d7256c02081.png)

Greengrass V1.x에서는 Docker connector를 이용하였고 V2.0에서는 Component의 Recipy의 environment variable에 정의된 registry에서 Docker Component를 생성하게 됩니다. 

추후 추가 예정 

## Reference

[Workshop - AWS IoT Greengrass V2](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US)

