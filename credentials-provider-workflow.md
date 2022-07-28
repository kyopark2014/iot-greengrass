# Credentials Provider Workflow


## Credentials Provider Workflow

![image](https://user-images.githubusercontent.com/52392004/181392716-4b78f2f8-202a-4190-a8e0-69a9fbd6b5ea.png)

1. The AWS IoT Core device makes an HTTPS request to the credentials provider for a security token. The request includes the device X.509 certificate for authentication.

2. The credentials provider forwards the request to the AWS IoT Core authentication and authorization module to validate the certificate and verify that the device has permission to request the security token.

3. If the certificate is valid and has permission to request a security token, the AWS IoT Core authentication and authorization module returns success. Otherwise, it sends an exception to the device.

4. After successfully validating the certificate, the credentials provider invokes the AWS Security Token Service (AWS STS) to assume the IAM role that you created for it.

5. AWS STS returns a temporary, limited-privilege security token to the credentials provider.

6. The credentials provider returns the security token to the device.

7. The device uses the security token to sign an AWS request with AWS Signature Version 4.

8. The requested service invokes IAM to validate the signature and authorize the request against access policies attached to the IAM role that you created for the credentials provider.

9. If IAM validates the signature successfully and authorizes the request, the request is successful. Otherwise, IAM sends an exception.

## Reference

[Credentials Provider Workflow](https://docs.aws.amazon.com/iot/latest/developerguide/authorizing-direct-aws.html)

