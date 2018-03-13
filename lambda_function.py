from __future__ import print_function
import os
import subprocess
import errno
import sys
import uuid
     
#Variables
tmpDir = "/tmp/inputSource"
pubDir = tmpDir + "/public"


def lambda_handler(event, context):
    siteGen(event)
    return 'Site Generated!'

def siteGen(event):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
    #Create directory structure
    subprocess.run(["mkdir", "-p", tmpDir + "/static"])    
    inputBucket = bucket
    dstBucket = inputBucket[6:]

    print('\n\nRunning Hugo generation on bucket: ' + inputBucket)
    print('Destination bucket will be: ' + dstBucket); 
    download_input(inputBucket, tmpDir)
    runHugo()
    upload_website(dstBucket, pubDir)

def download_input(inputBucket, tmpDir):
    print('Downloading Input!\n')
    command = ["./aws s3 sync s3://" + inputBucket + "/hugo/" + " " + tmpDir + "/"]
    try:
        subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        quit('Error downloading from input bucket')

def runHugo():
    print('Running Hugo!\n')
    subprocess.run(["./hugo", "-v", "--source=" + tmpDir, "--destination=" + pubDir])
    
def upload_website(dstBucket, pubDir):
    print('Publishing site!\n')
    command = ["./aws s3 sync --acl public-read --delete" + " " + pubDir + "/" + " " + "s3://" + dstBucket + "/"]
    try:
        subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        quit('Error uploading site')