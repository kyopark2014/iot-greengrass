# ML Component를 이용한 이미지 처리 

여기서는 [Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)에 따라 AWS의 public component인 DLRImageClassification을 이용하여 이미지에서 어떤 object를 추출하고자 합니다.

## DLRImageClassification 란?

[DLRImageClassification](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-component.html?icmpid=docs_gg_console)은 [Deep Learning Runtime](https://github.com/neo-ai/neo-ai-dlr)을 이용한 inference를 제공합니다. 

#### DLR 사용 예제 

```python
import dlr
import numpy as np

# Load model.
# /path/to/model is a directory containing the compiled model artifacts (.so, .params, .json)
model = dlr.DLRModel('/path/to/model', 'cpu', 0)

# Prepare some input data.
x = np.random.rand(1, 3, 224, 224)

# Run inference.
y = model.run(x)
```

이때의 [Recipt](https://github.com/kyopark2014/iot-greengrass/blob/main/recipe-DLRImageClassification.json)을 보면, "cat.jpeg"에 대한 classification 결과를 "aws.greengrass.ipc.mqttproxy"인 IPC service identifier를 사용하므로 "ml/dlr/image-classification"인 topic으로 publish를 하고 있음을 알 수 있습니다.  

## DLRImageClassification의 config 수정 

아래와 같이 Public Component의 config를 수정할 수 있습니다. 


1) [[Greengrass devices] - [Components] - [Public components]](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/components/public)로 진입하여 "aws.greengrass.DLRImageClassification"을 선택합니다. 

2) 우측 상단의 "Deploy"를 선택한 후에 현재 작업중인 deployment를 선택하고 [Next]를 선택합니다. 

3) [Specify target]에서 수정없이 [Next]를 선택합니다. 

4) [Select components]에서 [Public components]에 "aws.greengrass.DLRImageClassification"이 선택된지 확인후에 [Next]를 선택합니다. 

5) [Selected components]에서 "aws.greengrass.DLRImageClassification"을 선택후에 [Configure component]를 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/184886249-4870bebf-c8f0-42fc-82e8-79f8585e979d.png)

6) 아래처럼 [Configure to merge]를 수정후에 하단으로 이동하여 [Confirm]을 선택합니다. 

![image](https://user-images.githubusercontent.com/52392004/184886451-9e51a7e7-c769-47a5-9027-448517e197b8.png)

7) 이후로 수정없이 [Next]를 선택하다가 [Deploy]를 수행합니다. 

수정훈 결과를 [MQTT test client](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/test)로 이동하여 [Subscribe to a topic]에서 "ml/example/imgclassification"을 입력하여 확인합니다. 이때의 결과는 아래와 같습니다. 

![image](https://user-images.githubusercontent.com/52392004/184887802-1a336929-9f4a-4c9b-acc3-99e4c2a88b9c.png)




## Reference

[Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)
