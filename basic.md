# IoT Greengrass Basic

Edge에서 사용되어지는 IoT 디바이스들이 많아지면서, IT 담당자들은 수천개 또는 수백만개의 network endpoint를 개발 및 관리하여야 합니다. AWS Greengrass를 이용하면 Edge에 있는 IoT 디바이스들를 scalable 방법으로 효과적으로 관리할 수 있습니다. 

AWS Greengrass V2는 오픈소스 edge runtime으로 2022년에 re-invtent에서 소개되었습니다. AWS Greengrass를 통해 아래와 같은 효과를 볼 수 있습니다.
- 실시간으로 local event에 응답할 수 있습니다. 
- 네트워크 연결과 독립적으로 운영할 수 있습니다.
- AWS Cloud와 연결하여 다양한 서비스를 이용할 수 있습니다.
- 원격에서 모니터링을 할 수 있습니다. 
- IoT thing group를 화면 디바이스를 그룹으로 쉽게 organiza할 수 있고, 배포시 rollout/rollback등을 쉽게 할 수 있습니다. 
- 다양한 pre-built된 software component들을 사용 목적에 맞게 더하거나 삭제할 수 있습니다. 예) Stream manager
- Greengrass CLI를 이용하여 local 디바이스에서 어플리케이션을 개발하거나 디버깅 할 수 있습니다. 

<img width="905" alt="image" src="https://user-images.githubusercontent.com/52392004/182485948-796b6423-8cff-4e91-a89b-2aec21be86e5.png">

Greengrass Core는 local device와 OPC-UA, LoRA, Zigbee를 통해 연결될 수 있습니다. Data는 MQTT를 이용해 AWS IoT Core를 통해 라우팅되며, AWS Managed service에 의해 cloud와 device의 연결이 관리됩니다. 이렇게 함으로써 AWS 서비스인 S3, EC2, Sagemaker와 쉽게 연결할 수 있습니다. 

## AI with AWS Greengrass

Greengrass와 연결된 local camera는 실시간으로 물체를 인식하도록 할 수 있습니다. 이렇게 함으로써 사용자의 경험을 향상시키고, 새로운 가치를 제공 할 수 있습니다. 이러한 데이터는 AWS cloud의 machine learning model을 이용해 training되고 디바이스의 기능을 향상시킬 수 있습니다. 

네트워크가 오프라인이어도 local device에서 AI/ML model에 기반한 예측이 가능하며, 네트워크가 다시 연결되었을때 AWS Cloud로 데이터를 보내서 알고리즘을 향상 시킬 수 있습니다. 

## Reference

[AWS Greengrass Hardware Enables Connectivity for IoT Edge Devices](https://www.onlogic.com/company/io-hub/iot-edge-devices/amp/)

[AWS Announces a New Version of AWS Iot Greengrass](https://www.infoq.com/news/2020/12/aws-iot-greengrass-2-0/)

[AWS IoT Greengrass - Github](https://github.com/aws-greengrass)

[Announcing AWS IoT Greengrass 2.0 – With an Open Source Edge Runtime and New Developer Capabilities](https://www.stackovercloud.com/2020/12/15/announcing-aws-iot-greengrass-2-0-with-an-open-source-edge-runtime-and-new-developer-capabilities/)
