# Lambda Component

## Lambda 생성 

#### AWS Lambda mappings

- One Lambda to one component
- Refactor single AWS Lambda functions to multiple, dependent components

#### Import AWS Lambda functions to components

```c
aws greengrassv2 create-component-version --lambda-arn 
```

#### Map subscriptions to component via authorization templates


## Reference


[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)

[Tutorial creating hello world greengrass Lambda (in Python)](https://www.youtube.com/watch?v=jvQsygmzov0)

[rpi-greengrass](https://github.com/miman/rpi-greengrass/blob/master/hello-world/README.md)
