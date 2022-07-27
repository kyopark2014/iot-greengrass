# Greengrass Component

## Component의 특징

- 하나의 Component는 Receipe file과 Artifacts로 구성됩니다. 

- Component의 dependency를 yaml 파일 안에 ComponentDependencies에 정의 할 수 있습니다. 

- Component는 ComponentName과 ComponentVersion으로 구분합니다.

- Component states: RUNNING, FINISHED, ERRORED, BROKEN


## Receipe 예제

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

## Reference 

[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)
