# Greengrass Component

## Component의 특징

- 하나의 Component는 Recipe file과 Artifacts로 구성됩니다. 

- Component의 dependency를 yaml 파일 안에 ComponentDependencies에 정의 할 수 있습니다. 

- Component는 ComponentName과 ComponentVersion으로 구분합니다.

- Component states: RUNNING, FINISHED, ERRORED, BROKEN

- AWS에서 제공하는 Components: Nucleus, Greengrass CLI, Log manager, Stream manager, Local debug console, Secret manager, Secure tunneling 등이 있습니다. 

<img width="929" alt="image" src="https://user-images.githubusercontent.com/52392004/181392075-43f385db-222d-4506-9727-5f0aa7211619.png">


## Artifacts

component를 통해서 실행될 코드 부분인 Artifacts에는 스크립트, 컴파일된 코드, 정적 리소스등이 포함합니다. Component는 종속적으로 지정된 구성요소의 다른 artifacts도 사용할 수 있습니다. 


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

[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)
