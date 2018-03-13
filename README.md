# serverlessHugo
Deploy a hugo site automatically with AWS Lambda

![Diagram](https://raw.githubusercontent.com/richstokes/serverlessHugo/master/diagram.png)

## Overview
This is a packaged AWS Lambda function that will watch an S3 'inputBucket' for changes to a Hugo site. It will then run hugo within Lambda, and publish the results to a seperate, public S3 bucket.

This public S3 bucket will be enabled for static website hosting.

*Bonus fun!* Point a cloudfront instance at your static website hosting bucket to quickly and easily deploy your Hugo site with the AWS CDN.

&nbsp;

## Example deployment
Once set up, updating your Hugo website with this infrastructure is as simple as running an S3 sync command. e.g.

`aws s3 sync --delete /home/user/hugoSite/ s3://input.yourwebsite.com`


&nbsp;
## Requirements
1. Input bucket should be named 'input.yourwebsite.com'
2. Website bucket should be named 'yourwebsite.com'
3. Create a redirect website bucket for 'www.yourwebsite.com' if needed



### IAM Role
You should create a role for running this Lambda function. Give it the following two policies:

1. AWSLambdaBasicExecutionRole
2. Create Inline policy with the following access:-
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListAllMyBuckets"
            ],
            "Resource": [
                "arn:aws:s3:::*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::input.yourwebsite.com"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::input.yourwebsite.com/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::yourwebsite.com"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:DeleteObject",
                "s3:GetObject",
                "s3:PutObject",
                "s3:GetObjectAcl",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::yourwebsite.com/*"
            ]
        }
    ]
}
```
&nbsp;

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
            "Role": "arn:aws:iam::7023841xxxx:role/hugoLambdaExecRole",

            "Runtime": "python3.6",

            "CodeSize": 18075466,
            "FunctionName": "hugoPyLambda",
            "LastModified": "2018-03-13T18:48:48.424+0000",
            "Version": "$LATEST"
        }
    ]
}
```

&nbsp;

## Building the package yourself
package.zip contains the hugo executable, the AWS CLI program and lambda_function.py

You can recreate this package by

&nbsp;

## Credits
Thanks to the following sources: 
