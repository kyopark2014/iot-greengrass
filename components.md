# Greengrass Component

Greengrass component는 Greengrass core device를 설치(deploy)하는 소프트웨어 모듈입니다. Application, runtime installer 또는 device에서 실행되는 코드들은 모두 component로 표현됩니다. component들 사이에는 dependency가 있을 수 있습니다. 

## Component의 특징

- 하나의 Component는 Recipe file과 Artifacts로 구성됩니다. 

- Component의 dependency를 json 또는 yaml 파일 안에 ComponentDependencies에 정의 할 수 있습니다. 

- Component는 ComponentName과 ComponentVersion으로 구분합니다.

- Component states: RUNNING, FINISHED, ERRORED, BROKEN

- AWS에서 제공하는 Components: Nucleus, Greengrass CLI, Log manager, Stream manager, Local debug console, Secret manager, Secure tunneling 등이 있습니다. 

<img width="929" alt="image" src="https://user-images.githubusercontent.com/52392004/181392075-43f385db-222d-4506-9727-5f0aa7211619.png">


### Recipe

모든 component는 메타데이터를 정의하는 recipe를 가지고 있습니다. recipe는 compenent의 환경변수를 가지고 있고, 다른 component들과의 dependency와 lifecycle 및 platform 호환성을 기술합니다. 여기서 lifecycle은 component를 설치, 실행 및 종료(shot down)할때의 명령어를 정의 합니다. recipe는 json, yaml 파일포맷으로 정의되며, [AWS IoT Greengrass component recipe reference](https://docs.aws.amazon.com/greengrass/v2/developerguide/component-recipe-reference.html)에 상세하게 설명하고 있습니다. 



### Artifact

Component는 여러개의 artifacts를 가질수 있습니다. Artifacts에는 스크립트, 컴파일된 코드, 정적 리소스 등이 포함합니다. Component는 종속적으로 관계를 가지고 있는 다른 component의 artifacts도 사용할 수 있습니다. 

```java
"Artifacts": [
  {
    "URI": "s3://DOC-EXAMPLE-BUCKET/artifacts/com.example.MyDockerComponent/1.0.0/hello-world.tar"
  },
  {
    "URI": "s3://DOC-EXAMPLE-BUCKET/hello_world.zip",
    "Unarchive": "ZIP"
  },
  {
    "URI": "s3://DOC-EXAMPLE-BUCKET/hello_world_linux.py"
  },
  {
    "URI": "docker:public.ecr.aws/cloudwatch-agent/cloudwatch-agent:latest"
  },
  {
    "URI": "docker:mysql:8.0"
  },
  {
    "URI": "s3://DOC-EXAMPLE-BUCKET/folder/docker-compose.yaml"
  }
]
```

## Component types

Component는 아래와 같은 Type을 가지고 있습니다.

- Nucleus (aws.greengrass.nucleus): IoT Greengrass Core softweare를 구동하는 최소한의 기능을 제공합니다.

- Plugin (aws.greengrass.plugin): Nucleus가 JVM에서 plugin을 구동합니다. plugin component는 버전이 바뀔때마다 재실행됩니다. plugin component를 설치하거나 실행하려면 nucleus의 configure을 수정하여야 합니다. AWS에서는 necleus와 직접적으로 interface를 할 수 있도록 여러가지의 plugin component들을 제공하고 있습니다. 또한, plugin component는 neclues와 로그를 공유합니다. 

- Generic (aws.greengrass.generic): component의 기본 type으로 lifecycle scripts로 정의되고, neclues가 실행합니다. 

- Lambda (aws.greengrass.lambda): Necleus는 Lambda launcher component를 이용하여 lambda 함수를 실행합니다. 


### [AWS-provided components](https://docs.aws.amazon.com/greengrass/v2/developerguide/public-components.html)

- Greengrass nucleus: The nucleus of the AWS IoT Greengrass Core software. Use this component to configure and update the software on your core devices.
- Client device auth: Enables local IoT devices, called client devices, to connect to the core device.
- CloudWatch metrics: Publishes custom metrics to Amazon CloudWatch.
- AWS IoT Device Defender: Notifies administrators of changes in the state of the Greengrass core device to identify unusual behavior.
- Docker application manager: Enables AWS IoT Greengrass to download Docker images from Docker Hub and Amazon Elastic Container Registry (Amazon ECR).
- Edge connector for Kinesis Video Streams: Reads video feeds from local cameras, publishes the streams to Kinesis Video Streams, and displays the streams in Grafana dashboards with AWS IoT TwinMaker.
- Greengrass CLI: Provides a command-line interface that you can use to create local deployments and interact with the Greengrass core device and its components.
- IP detector: 	Reports MQTT broker connectivity information to AWS IoT Greengrass, so client devices can discover how to connec
- Kinesis Data Firehose: Publishes data through Amazon Kinesis Data Firehose delivery streams to destinations in the AWS Cloud.
- Lambda launcher: Handles processes and environment configuration for Lambda functions.
- Lambda manager: Handles interprocess communication and scaling for Lambda functions.
- Lambda runtimes: Provides artifacts for each Lambda runtime.
- Legacy subscription router: Manages subscriptions for Lambda functions that run on AWS IoT Greengrass V1.
- Local debug console: Provides a local console that you can use to debug and manage the Greengrass core device and its components.
- Log manager: Collects and uploads logs on the Greengrass core device.
- Machine learning components: Provides machine learning models and sample inference code that you can use to perform machine learning inference on Greengrass core devices.
- Modbus-RTU protocol adapter: Polls information from local Modbus RTU devices.
- Nucleus telemetry emitter: Publishes system health telemetry data gathered from the nucleus to a local topic or to an AWS IoT Core MQTT topic.
- MQTT bridge: Relays MQTT messages between client devices, local AWS IoT Greengrass publish/subscribe, and AWS IoT Core.
- MQTT 3.1.1 broker (Moquette): Runs an MQTT 3.1.1 broker that handles messages between client devices and the core device.
- MQTT 5 broker (EMQX): Runs an MQTT 5 broker that handles messages between client devices and the core device.
- PKCS#11 provider: Enables Greengrass components to to access a private key and certificate that you securely store in a hardware security module (HSM).
- Secret manager: Deploys secrets from AWS Secrets Manager secrets so that you can securely use credentials, such as passwords, in custom components on the Greengrass core device.
- Secure tunneling: Enables AWS IoT secure tunneling connections that you can use to establish bidrectional communications with Greengrass core devices that are behind restricted firewall
- Shadow manager: Enables interaction with shadows on the core device. It manages shadow document storage and also the synchronization of local shadow states with the AWS IoT Device Shadow service.
- Amazon SNS: Publishes messages to Amazon SNS topics.
- Stream manager: Streams high-volume data from local sources to the AWS Cloud.
- Systems Manager Agent: Manage the core device with AWS Systems Manager, which enables you to patch devices, run commands, and more.
- Token exchange service: Provides AWS credentials that you can use to interact with AWS services.
- IoT SiteWise OPC-UA collector: Collects data from OPC-UA servers.
- IoT SiteWise OPC-UA data source simulator: Runs a local OPC-UA server that generates sample data.
- [IoT SiteWise publisher](https://github.com/kyopark2014/aws-iot-sitewise/blob/main/sitewise-publisher.md): Publishes data to the AWS Cloud.
- IoT SiteWise processor: Processes data on the Greengrass core devices.




## Recipe 예제

```java
---
RecipeFormatVersion: 2020-01-25
ComponentName: demo.example.hello_world
ComponentVersion: '1.0.0'
ComponentDescription: My first AWS IoT Greengrass component.
ComponentPublisher: Amazon
ComponentDependencies:
  aws.greengrass.TokenExchangeService:
    VersionRequirement: '>=0.0.0'
    DependencyType: HARD
ComponentConfiguration:
  DefaultConfiguration:
    Message: world
Manifests:
  - Platform:
      os: linux
    Lifecycle:
      Run: |
        while true; do
          python3 {artifacts:path}/hello_world.py \
            '{configuration:/Message}’
          sleep 5
        done
     Artifacts:
       - URI: s3://BUCKET/artifacts/demo.example.hello_world/…
```


```java
{
  "RecipeFormatVersion": "2020-01-25",
  "ComponentName": "com.example.ImgClassification",
  "ComponentVersion": "1.0.0",
  "ComponentType": "aws.greengrass.generic",
  "ComponentDescription": "Custom Image classification inference component using DLR.",
  "ComponentPublisher": "AWS",
  "ComponentConfiguration": {
    "DefaultConfiguration": {
      "accessControl": {
        "aws.greengrass.ipc.mqttproxy": {
          "com.example.Pub:publisher:1": {
            "policyDescription": "Allows access to publish to ml/example/imgclassification topic.",
            "operations": [
              "aws.greengrass#PublishToIoTCore"
            ],
            "resources": [
              "ml/example/imgclassification"
            ]
          }
        }
      }
    }
  },
  "Manifests": [
    {
      "Platform": {
        "os": "linux"
      },
      "Lifecycle": {
        "Install": {
          "RequiresPrivilege": true,
          "Script": "/bin/bash {artifacts:decompressedPath}/my-model/install.sh",
          "timeout": "900"
        },
        "setEnv": {
          "MODEL_CPU_DIR": "{artifacts:decompressedPath}/my-model/model_cpu",
          "MODEL_GPU_DIR": "{artifacts:decompressedPath}/my-model/model_gpu",
          "SAMPLE_IMAGE_DIR": "{artifacts:decompressedPath}/my-model/sample_images"
        },
        "Run": {
          "RequiresPrivilege": true,
          "script": "/bin/bash {artifacts:decompressedPath}/my-model/run.sh"
        }
      },
      "Artifacts": [
        {
          "Uri": "s3://greengrass-abc/ggv2/artifacts/my-model.zip",
          "Digest": "Sample4YJ2HLCBPcVZFMFBmsHBLm9E4dX8neLXS3mVCA=",
          "Algorithm": "SHA-256",
          "Unarchive": "ZIP",
          "Permission": {
            "Read": "OWNER",
            "Execute": "NONE"
          }
        }
      ]
    }
  ],
  "Lifecycle": {}
}
```

#### Necleus를 위한 recipe.yaml

```yaml
---
RecipeFormatVersion: "2020-01-25"
ComponentName: "aws.greengrass.Nucleus"
ComponentVersion: "2.7.0"
ComponentType: "aws.greengrass.nucleus"
ComponentDescription: "Core functionality for device side orchestration of deployments\
  \ and lifecycle management for execution of Greengrass components and applications.\
  \ This includes features such as starting, stopping, and monitoring execution of\
  \ components and apps, interprocess communication server for communication between\
  \ components, component installation and configuration management."
ComponentPublisher: "AWS"
ComponentConfiguration:
  DefaultConfiguration:
    jvmOptions: ""
    iotDataEndpoint: ""
    iotCredEndpoint: ""
    greengrassDataPlanePort: "8443"
    awsRegion: ""
    iotRoleAlias: ""
    mqtt: {}
    networkProxy: {}
    runWithDefault: {}
    deploymentPollingFrequencySeconds: "15"
    componentStoreMaxSizeBytes: "10000000000"
    platformOverride: {}
Manifests:
- Platform:
    os: "linux"
  Lifecycle:
    bootstrap:
      requiresPrivilege: true
      script: "\nset -eu\nKERNEL_ROOT=\"{kernel:rootPath}\"\nUNPACK_DIR=\"{artifacts:decompressedPath}/aws.greengrass.nucleus\"\
        \nrm -r \"$KERNEL_ROOT\"/alts/current/*\necho \"{configuration:/jvmOptions}\"\
        \ > \"$KERNEL_ROOT/alts/current/launch.params\"\nln -sf \"$UNPACK_DIR\" \"\
        $KERNEL_ROOT/alts/current/distro\"\nexit 100"
  Artifacts: []
- Platform:
    os: "darwin"
  Lifecycle:
    bootstrap:
      requiresPrivilege: true
      script: "\nset -eu\nKERNEL_ROOT=\"{kernel:rootPath}\"\nUNPACK_DIR=\"{artifacts:decompressedPath}/aws.greengrass.nucleus\"\
        \nrm -r \"$KERNEL_ROOT\"/alts/current/*\necho \"{configuration:/jvmOptions}\"\
        \ > \"$KERNEL_ROOT/alts/current/launch.params\"\nln -sf \"$UNPACK_DIR\" \"\
        $KERNEL_ROOT/alts/current/distro\"\nexit 100"
  Artifacts: []
- Platform:
    os: "windows"
  Lifecycle:
    bootstrap:
      requiresPrivilege: true
      script: "copy {kernel:rootPath}\\alts\\current\\distro\\bin\\greengrass.xml\
        \ {artifacts:decompressedPath}\\aws.greengrass.nucleus\\bin\\greengrass.xml&\
        \ del /q {kernel:rootPath}\\alts\\current\\*&& for /d %x in ({kernel:rootPath}\\\
        alts\\current\\*) do @rd /s /q \"%x\"&& echo {configuration:/jvmOptions} >\
        \ {kernel:rootPath}\\alts\\current\\launch.params&& mklink /d {kernel:rootPath}\\\
        alts\\current\\distro {artifacts:decompressedPath}\\aws.greengrass.nucleus&&\
        \ exit 100"
  Artifacts: []
Lifecycle: {}
```


## Reference 

[Develop AWS IoT Greengrass components](https://docs.aws.amazon.com/greengrass/v2/developerguide/develop-greengrass-components.html#component-types)

[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)

[AWS-provided components](https://docs.aws.amazon.com/greengrass/v2/developerguide/public-components.html)
