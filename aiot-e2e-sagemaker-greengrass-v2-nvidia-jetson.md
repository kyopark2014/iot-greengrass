# aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson

[create_gg_component.sh](https://github.com/aws-samples/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson/blob/main/ggv2-deploy-cloud/create_gg_component.sh)에 대한 상세 내용을 기술합니다. 

create_gg_component.sh의 내용은 아래와 같습니다. 

```script
#!/bin/bash

echo ==--------Install Dedendencies---------==
# npm install     
sudo apt install jq
npm --version
jq --version
echo .

echo ==--------Configurations---------==
COMPONENT_NAME=$(cat config.json | jq -r '.Component.ComponentName')
COMPONENT_VERSION=$(cat config.json | jq -r '.Component.ComponentVersion')
ENABLE_SEND_MESSAGE=$(cat config.json | jq -r '.Component.SendMessage')
PREDICTION_INTERVAL_SECS=$(cat config.json | jq -r '.Component.PredictionIntervalSecs')
TIMEOUT=$(cat config.json | jq -r '.Component.Timeout')

S3_BUCKET=$(cat config.json | jq -r '.Artifacts.S3Bucket')
S3_PREFIX=$(cat config.json | jq -r '.Artifacts.S3Prefix')
S3_PREFIX2=${S3_PREFIX//\//\\/}
ZIP_ARCHIVE_NAME=$(cat config.json | jq -r '.Artifacts.ZipArchiveName')

USE_GPU=$(cat config.json | jq -r '.Parameters.UseGPU')
SCORE_THRESHOLD=$(cat config.json | jq -r '.Parameters.ScoreThreshold')
MAX_NUM_CLASSES=$(cat config.json | jq -r '.Parameters.MaxNumClasses')
MODEL_INPUT_SHAPE=$(cat config.json | jq -r '.Parameters.ModelInputShape')

echo component name: $COMPONENT_NAME
echo component version: $COMPONENT_VERSION
echo zip archive name: $ZIP_ARCHIVE_NAME
echo .

# s3 bucket
S3_PATH="s3://${S3_BUCKET}/${S3_PREFIX}"
S3_FILEPATH="${S3_PATH}/${ZIP_ARCHIVE_NAME}.zip"
S3_FILEPATH2=${S3_FILEPATH//\//\\/}

if aws s3api head-bucket --bucket "$S3_BUCKET" 2>/dev/null; then
    echo ==--------Bucket Already Exists---------==
else
    echo ==--------Create S3 Bucket---------==   
    aws s3 mb $S3_PATH
fi

# json recipe
echo ==--------JSON Recipe---------==
cd recipes
OLD_RECIPE_JSON=$(ls ${COMPONENT_NAME}*.json)
NEW_RECIPE_JSON=${COMPONENT_NAME}-${COMPONENT_VERSION}.json
mv ${OLD_RECIPE_JSON} ${NEW_RECIPE_JSON}

sed -i "s/\(\"UseGPU\"\)\(.*\)/\1: \"${USE_GPU}\",/g" ${NEW_RECIPE_JSON}
sed -i "s/\(\"URI\"\)\(.*\)/\1: \"${S3_FILEPATH2}\",/g" ${NEW_RECIPE_JSON}
sed -i "s/my-model/${ZIP_ARCHIVE_NAME}/g" ${NEW_RECIPE_JSON} 
sed -i "s/\(\"ComponentVersion\"\)\(.*\)/\1: \"${COMPONENT_VERSION}\",/g" ${NEW_RECIPE_JSON}

echo old json recipe: $OLD_RECIPE_JSON
echo new json recipe: $NEW_RECIPE_JSON
cd ..
echo .

# config_utils.py
echo ==--------Config Utils---------==
CONFIG_PY="artifacts/config_utils.py"

sed -i "s/\(USE_GPU\)\(.*\)/\1 = ${USE_GPU}/g" ${CONFIG_PY}
sed -i "s/\(SCORE_THRESHOLD\)\(.*\)/\1 = ${SCORE_THRESHOLD}/g" ${CONFIG_PY}
sed -i "s/\(MAX_NO_OF_RESULTS\)\(.*\)/\1 = ${MAX_NUM_CLASSES}/g" ${CONFIG_PY}
sed -i "s/\(SHAPE\)\(.*\)/\1 = ${MODEL_INPUT_SHAPE}/g" ${CONFIG_PY}
sed -i "s/\(TIMEOUT\)\(.*\)/\1 = ${TIMEOUT}/g" ${CONFIG_PY}
sed -i "s/\(DEFAULT_PREDICTION_INTERVAL_SECS\)\(.*\)/\1 = ${PREDICTION_INTERVAL_SECS}/g" ${CONFIG_PY}
sed -i "s/\(ENABLE_SEND_MESSAGE\)\(.*\)/\1 = ${ENABLE_SEND_MESSAGE}/g" ${CONFIG_PY}

echo .

echo ==--------Compress Artifacts---------==
cd artifacts
zip ${ZIP_ARCHIVE_NAME}.zip -r .

echo ==--------Uploading to $S3_FILEPATH---------== 
aws s3 cp ${ZIP_ARCHIVE_NAME}.zip ${S3_FILEPATH}
rm ${ZIP_ARCHIVE_NAME}.zip
echo .

echo ==--------Creating Component---------==
cd ../recipes 
aws greengrassv2 create-component-version --inline-recipe fileb://${COMPONENT_NAME}-${COMPONENT_VERSION}.json 
echo .
```

실제 실행 로그는 아래와 같습니다.

```java
$ ./create_gg_component.sh 
==--------Install Dedendencies---------==
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages were automatically installed and are no longer required:
  libc-ares2 libhttp-parser2.7.1
Use 'sudo apt autoremove' to remove them.
The following additional packages will be installed:
  libjq1 libonig4
The following NEW packages will be installed:
  jq libjq1 libonig4
0 upgraded, 3 newly installed, 0 to remove and 6 not upgraded.
Need to get 276 kB of archives.
After this operation, 930 kB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://ap-northeast-2.ec2.archive.ubuntu.com/ubuntu bionic/universe amd64 libonig4 amd64 6.7.0-1 [119 kB]
Get:2 http://ap-northeast-2.ec2.archive.ubuntu.com/ubuntu bionic/universe amd64 libjq1 amd64 1.5+dfsg-2 [111 kB]
Get:3 http://ap-northeast-2.ec2.archive.ubuntu.com/ubuntu bionic/universe amd64 jq amd64 1.5+dfsg-2 [45.6 kB]
Fetched 276 kB in 0s (17.4 MB/s)
Selecting previously unselected package libonig4:amd64.
(Reading database ... 110590 files and directories currently installed.)
Preparing to unpack .../libonig4_6.7.0-1_amd64.deb ...
Unpacking libonig4:amd64 (6.7.0-1) ...
Selecting previously unselected package libjq1:amd64.
Preparing to unpack .../libjq1_1.5+dfsg-2_amd64.deb ...
Unpacking libjq1:amd64 (1.5+dfsg-2) ...
Selecting previously unselected package jq.
Preparing to unpack .../jq_1.5+dfsg-2_amd64.deb ...
Unpacking jq (1.5+dfsg-2) ...
Setting up libonig4:amd64 (6.7.0-1) ...
Setting up libjq1:amd64 (1.5+dfsg-2) ...
Setting up jq (1.5+dfsg-2) ...
Processing triggers for man-db (2.8.3-2ubuntu0.1) ...
Processing triggers for libc-bin (2.27-3ubuntu1.6) ...
8.11.0
jq-1.5-1-a5b5cbe
.
==--------Configurations---------==
component name: com.example.ImgClassification
component version: 1.0.0
zip archive name: my-model
.
==--------Bucket Already Exists---------==
==--------JSON Recipe---------==
mv: 'com.example.ImgClassification-1.0.0.json' and 'com.example.ImgClassification-1.0.0.json' are the same file
old json recipe: com.example.ImgClassification-1.0.0.json
new json recipe: com.example.ImgClassification-1.0.0.json
.
==--------Config Utils---------==
.
==--------Compress Artifacts---------==
  adding: requirements.txt (deflated 5%)
  adding: run.sh (deflated 19%)
  adding: model_cpu/ (stored 0%)
  adding: model_cpu/IOC-INF/ (stored 0%)
  adding: model_cpu/IOC-INF/metadata.json (deflated 21%)
  adding: model_cpu/2004195752_0_Neo.so (deflated 74%)
  adding: model_cpu/libdlr.so (deflated 60%)
  adding: model_cpu/2004195752_0_Neo.meta (deflated 77%)
  adding: model_cpu/dlr.h (deflated 83%)
  adding: model_cpu/manifest (deflated 49%)
  adding: model_cpu/2004195752_0_Neo.params (deflated 7%)
  adding: model_cpu/2004195752_0_Neo.json (deflated 94%)
  adding: model_cpu/compiled.pt (deflated 56%)
  adding: model_cpu/sample_input.pkl (deflated 100%)
  adding: inference.py (deflated 60%)
  adding: classes_dict.json (deflated 53%)
  adding: test_dlr.py (deflated 56%)
  adding: install.sh (deflated 39%)
  adding: utils.py (deflated 59%)
  adding: IPCUtils.py (deflated 69%)
  adding: config_utils.py (deflated 50%)
  adding: sample_images/ (stored 0%)
  adding: sample_images/red_normal.jpg (deflated 0%)
  adding: sample_images/brown_abnormal_chinese.jpg (deflated 0%)
  adding: sample_images/brown_normal_korean.jpg (deflated 0%)
  adding: sample_images/red_abnormal.jpg (deflated 0%)
  adding: sample_images/brown_abnormal_korean.jpg (deflated 0%)
  adding: sample_images/brown_normal_chinese.jpg (deflated 0%)
==--------Uploading to s3://mybucket-123456789012/ggv2/artifacts/my-model.zip---------==
upload: ./my-model.zip to s3://mybucket-123456789012/ggv2/artifacts/my-model.zip
.
==--------Creating Component---------==
{
    "arn": "arn:aws:greengrass:ap-northeast-2:123456789012:components:com.example.ImgClassification:versions:1.0.0",
    "componentName": "com.example.ImgClassification",
    "componentVersion": "1.0.0",
    "creationTimestamp": 1660620526.199,
    "status": {
        "componentState": "REQUESTED",
        "message": "NONE",
        "errors": {},
        "vendorGuidance": "ACTIVE",
        "vendorGuidanceMessage": "NONE"
    }
}
.
echo .
```

관련로그는 아래와 같습니다. 

```java
$ S3_PREFIX=$(cat config.json | jq -r '.Artifacts.S3Prefix')
$ S3_PREFIX2=${S3_PREFIX//\//\\/}
$ echo $S3_PREFIX
ggv2/artifacts
$ echo $S3_PREFIX2
ggv2\/artifacts
```
$ S3_PREFIX2=${S3_PREFIX//\//\\/}
