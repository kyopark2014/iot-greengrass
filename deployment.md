# Component Deployment

## Component 생성

1. Component의 artifact를 S3 Bucket에 업로드합니다.

2. recipe에 S3의 URI를 포함합니다.

3. artifact와 recipe를 활용하여, 클라우드 상에 component를 생성할 수 있습니다. 이렇게 cloud에 등록된 component를 다른 device에 배포할 수 있습니다. 

![image](https://user-images.githubusercontent.com/52392004/182487907-91593858-a4ef-4010-97ae-320b4dfd5ad9.png)


## 배포방법

Component를 배포하기 위해서는 deployment를 생성하여야 합니다. Deployment는 Greengrass core device에서 실행되는 component 및 configuration을 정의합니다. 

AWS IoT Thing Group을 이용하여 deployment를 수행할 Core device들의 목록을 지정할 수 있습니다. 

Active deployment가 있는 thing group에 새 core device를 추가하면 AWS IoT Greengrass V2가 해당 deployment를 해당 core device로 보냅니다. 이때, Deployment가 roll-out 되는 속도와 deployment를 실패하는 조건을 구성 가능합니다. 



![image](https://user-images.githubusercontent.com/52392004/182489658-535afb91-6c8a-49a8-86aa-ce19addcdd30.png)
