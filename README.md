# serverlessHugo
Deploy a hugo site automatically with AWS Lambda. 

&nbsp;

![Diagram](https://raw.githubusercontent.com/richstokes/serverlessHugo/master/diagram.png)

## Overview
This is a packaged AWS Lambda function that will watch an S3 'inputBucket' for changes to a Hugo site. It will then run hugo within Lambda, and publish the results to a seperate, public S3 bucket.

This public S3 bucket will be enabled for static website hosting.

*Bonus fun!* Point a cloudfront instance at your static website hosting bucket to quickly and easily deploy your Hugo site with the AWS CDN.

&nbsp;

## Example deployment
Once set up, updating your Hugo website with this infrastructure is as simple as running an S3 sync command. e.g.

`aws s3 sync --delete /home/user/hugoSite/ s3://input.yourwebsite.com/hugo`


&nbsp;
## Requirements
1. Input bucket should be named 'input.yourwebsite.com'
2. Store/sync your raw hugo files to s3://input.yourwebsite.com/hugo
3. Website bucket should be named 'yourwebsite.com'
4. Create a redirect website bucket for 'www.yourwebsite.com' if needed



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
3. Set handler as 'lambda_function.lambda_handler'
3. Add S3 triggers for 'ObjectCreated' & 'ObjectRemoved' against your input bucket
3. Configure lambda function to use the IAM role above
4. 60 Second timeout
5. Runtime = python3.6

&nbsp;

## Building the deployment package yourself
package.zip contains the hugo executable, the AWS CLI program and lambda_function.py as well as the usual python libraries. 

You can recreate this package with the following:
&nbsp;

1. Spin up an EC2 Amazon Linux instance
2. Install python3.6
```
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz
tar xJf Python-3.6.0.tar.xz
cd Python-3.6.0 && ./configure && make && sudo make install
```
3. Create virtualenv for Python 3.6
```
sudo pip install --upgrade virtualenv
virtualenv -p python3 MYVENV
source MYVENV/bin/activate
```
4. Download & extract Hugo's Linux x64 package
```
wget https://github.com/gohugoio/hugo/releases/download/v0.37.1/hugo_0.37.1_Linux-64bit.tar.gz
tar xfvz hugo_0.37.1_Linux-64bit.tar.gz
mv hugo ~
```
4. Install AWS CLI
```
pip install awscli
cp ~/MYVENV/bin/aws ~
cd ~
```
5. Modify AWS CLI shebang to play nice on Lambda
```
perl -pi -e '$_ = "#!/usr/bin/python\n" if $. == 1' aws
```

5. Create deployment package .zip file
```
zip -g package.zip hugo
zip -g package.zip aws
zip -g package.zip lambda_function.py
cd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -r9 ~/package.zip *
```

## Credits
Big thanks to the following resources: 
* https://alestic.com/2016/11/aws-lambda-awscli/
* https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
* http://bezdelev.com/post/hugo-aws-lambda-static-website/
* https://medium.com/@bezdelev/how-to-test-a-python-aws-lambda-function-locally-with-pycharm-run-configurations-6de8efc4b206


