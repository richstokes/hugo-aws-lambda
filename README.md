# serverlessHugo
Deploy a hugo site automatically with AWS Lambda

![Diagram](https://raw.githubusercontent.com/richstokes/serverlessHugo/master/diagram.png)

## Overview
This is a packaged AWS Lambda function that will watch an S3 'inputBucket' for changes to a Hugo site. It will then run hugo within Lambda, and publish the results to a seperate, public S3 bucket.

This public S3 bucket will be enabled for static website hosting.

Bonus fun: Point a cloudfront instance at your static website hosting bucket to quickly and easily deploy your Hugo site with the AWS CDN!


## Example deployment
Once set up, updating your Hugo website with this infrastructure is as simple as running an S3 sync command. e.g.

`aws s3 sync --delete /home/user/hugoSite/ s3://input.yourwebsite.com`


## Requirements
1. Input bucket should be named 'input.yourwebsite.com'
2. Website bucket should be named 'yourwebsite.com'

### IAM Role


## Installing Lambda function
1. Create a new lambda function
2. Upload package.zip
3. Configure as below


```{
    "Functions": [
        {
            "TracingConfig": {
                "Mode": "PassThrough"
            },
            "VpcConfig": {
                "SubnetIds": [],
                "SecurityGroupIds": []
            },
            "Description": "Generate and publish hugo site",
            "Timeout": 60,
            "Handler": "lambda_function.lambda_handler",
            "MemorySize": 128,
            "Role": "arn:aws:iam::7023841xxxxx:role/hugoLambdaExecRole",

            "Runtime": "python3.6",

            "CodeSize": 18075466,
            "FunctionName": "hugoPyLambda",
            "LastModified": "2018-03-13T18:48:48.424+0000",
            "Version": "$LATEST"
        }
    ]
}
```

## Credits
Thanks to the following sources: 
