const iotsdk = require('aws-greengrass-core-sdk');

const GROUP_ID = process.env.GROUP_ID;
const THING_NAME = process.env.AWS_IOT_THING_NAME;
const THING_ARN = process.env.AWS_IOT_THING_ARN;

exports.handler = async (event) => {
    console.log('## ENVIRONMENT VARIABLES: ' + JSON.stringify(process.env));
    console.log('## EVENT: ' + JSON.stringify(event));
    
    const response = {
        statusCode: 200,
        body: JSON.stringify(event),
    };
    return response;
};