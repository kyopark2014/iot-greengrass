# ML component를 이용한 이미지 처리 

여기서는 [Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)에 따라 AWS의 public component인 DLRImageClassification을 이용하여 이미지에서 어떤 object를 추출하고자 합니다.

## DLRImageClassification

[DLRImageClassification](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-component.html?icmpid=docs_gg_console)은 [Deep Learning Runtime](https://github.com/neo-ai/neo-ai-dlr)을 이용한 inference를 제공합니다. 

#### DLR 사용 방법

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


1) [Greengrass Deployment](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/deployments)로 진입하여 
현재 
현재 작


1) [aws.greengrass.DLRImageClassification](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/components/public/aws.greengrass.DLRImageClassification/versions/2.1.8)을 deploy 합니다. 



## Reference

[Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)
