#!/usr/bin/env python
import os
import sys
import subprocess
import stat
import argparse
import string
import random
import time
from shutil import which

#Create random strings for default values
def random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

default_serverstring = random_string(10)
default_rid_replace = random_string(8)


#Static variables
aws_credentials = "~/.aws/credentials"
variablefile = "variables.tf"
instancefile = "instances.tf"
securitygroupsfile = "security_groups.tf"
ansibleplaybookfile = "ansible/phish-playbook.yml"
pythonfile = "autosneakphish.py"
publickey = ""
keyname = ""
sestffile = "ses.tf"
finalconfig = "finalconfig.sh"
notfoundfile = "ansible/downloads/404.html"

default_serverstring = random_string(10)
default_rid_replace = random_string(8)
default_private_key = random_string(8)
current_serverstring = "serverstring1"
current_rid = "rid_replace1"
current_domain = "domainstring1"
current_gophish_subdomain = "go_substring1" 
current_mx_subdomain = "mx_substring1" 
current_ami = "amistring1"
current_private_key = "private_keystring1" 
current_whitelist_cidr = "whitelist_cidrstring1"
current_zone_id = "zone_idstring1"
current_vpc_id = "vpc_idstring1"
current_title = "Negative Ghost Rider"
current_body = "This page doesn't exist or your not cool enough to see it. Return to Go and do not collect $200"
current_public_key = "publickey_replacer"
current_key_name = "keyname_replacer"
parser = argparse.ArgumentParser(description='''Automated evasive phishing infrastructure tool.''')

parser.add_argument("-s", "--serverstring", required=False, help="Your Servername and Header replacement string", default=default_serverstring)
parser.add_argument("-r", "--rid_replace", required=False, help="Your rid parameter replacement string", default=default_rid_replace)
parser.add_argument("-d", "--domain", required=True, help="Your SMTP sending domain name")
parser.add_argument("-g", "--gophish_subdomain", required=False, help="Your GoPhish landing page sub-domain", default="www")
parser.add_argument("-m", "--mx_subdomain", required=False, help="Your MX sub-domain", default="mx")
parser.add_argument("-a", "--amistring", required=True, help="Your ami")
parser.add_argument("-p", "--private_key", required=False, help="Your aws private key", default=default_private_key)
parser.add_argument("-w", "--whitelist_cidr", required=True, help="Your Public IP address for connecting to infrastructure")
parser.add_argument("-z", "--zone_id", required=True, help="Your AWS zone_id")
parser.add_argument("-v", "--vpc_id", required=True, help="Your AWS vpc id")
parser.add_argument("-t", "--title", required=True, help="Customize your 404 file Title")
parser.add_argument("-b", "--body", required=True, help="Customize your 404 file text")

args = parser.parse_args()

keyname = args.private_key

#Cleanup known hosts file from any prior infrastructure builds
subprocess.run(['ssh-keygen -f "~/.ssh/known_hosts" -R "' + args.gophish_subdomain + '.' + args.domain + '"'], shell=True)

#Create key pair to import into aws
subprocess.run(['terraform init'], shell=True)
subprocess.run(['ssh-keygen -b 2048 -t ed25519 -f ./' + args.private_key + ' -q -N ""'], shell=True)


#Check if private key exists
if os.path.isfile(args.private_key) is False:
    print("Please obtain an aws private key file and place it in the autosneakphish directory")
    sys.exit()
else:
    pass


#Ensure Private Key has correct permissions
checkpermissions = os.stat(args.private_key)
octal =  oct(checkpermissions.st_mode)
finalperm = octal[-4:]

if finalperm != "0600":
    os.chmod(args.private_key, 0o600)
else:
    pass


#Load the public key into our variable for later use
with open(args.private_key + '.pub') as file:
    publickey = file.read().replace('\n', ' ')

#Ensure aws credentials have been supplied to awscli
if os.path.isfile(aws_credentials) is not False:
    print("Please run aws configure and enter your credentials")
    sys.exit()
else:
    pass

#String replacement function
def replacer(current, replacement, filename):

    with open(filename, 'r') as file:
        data = file.read()
        data = data.replace(current, replacement)
    with open(filename, 'w') as file:
        file.write(data)
    return 0

# Replacing variables
replacer(current_serverstring, args.serverstring, ansibleplaybookfile)
replacer(current_rid, args.rid_replace, ansibleplaybookfile)
replacer(current_domain, args.domain, variablefile)
replacer(current_domain, args.domain, ansibleplaybookfile)
replacer(current_domain, args.domain, finalconfig)
replacer(current_gophish_subdomain, args.gophish_subdomain, finalconfig)
replacer(current_gophish_subdomain, args.gophish_subdomain, sestffile)
replacer(current_gophish_subdomain, args.gophish_subdomain, ansibleplaybookfile)
replacer(current_mx_subdomain, args.mx_subdomain, variablefile)
replacer(current_ami, args.amistring, variablefile)
replacer(current_private_key, args.private_key, variablefile)
replacer(current_public_key, publickey, securitygroupsfile)
replacer(current_key_name, keyname, securitygroupsfile)
replacer(current_whitelist_cidr, args.whitelist_cidr, variablefile)
replacer(current_zone_id, args.zone_id, variablefile)
replacer(current_vpc_id, args.vpc_id, variablefile)
replacer(current_title, args.title, notfoundfile)
replacer(current_body, args.body, notfoundfile)


#Preparing the script for a second run
replacer(current_serverstring, args.serverstring, pythonfile)
replacer(current_rid, args.rid_replace, pythonfile)
replacer(current_domain, args.domain, pythonfile)
replacer(current_gophish_subdomain, args.gophish_subdomain, pythonfile)
replacer(current_mx_subdomain, args.mx_subdomain, pythonfile)
replacer(current_ami, args.amistring, pythonfile)
replacer(current_private_key, args.private_key, pythonfile)
replacer(current_public_key, publickey, pythonfile)
replacer(current_key_name, keyname, pythonfile)
replacer(current_whitelist_cidr, args.whitelist_cidr, pythonfile)
replacer(current_zone_id, args.zone_id, pythonfile)
replacer(current_vpc_id, args.vpc_id, pythonfile)
replacer(current_title, args.title, pythonfile)
replacer(current_body, args.body, pythonfile)


#Run Terraform
subprocess.run(["terraform", "apply"])

#Final Configuration of phishing server
subprocess.Popen(['ssh -o StrictHostKeyChecking=no -i ' + args.private_key + ' ubuntu@' + args.gophish_subdomain + '.' + args.domain + ' bash -s < finalconfig.sh'], shell=True, stdout=subprocess.PIPE)

#Wait for configuration to complete so that we can port forward the gophish admin server
time.sleep(120)

#Utilize ssh to port forward the gophish admin server
subprocess.run(['ssh -o StrictHostKeyChecking=no -L 3333:localhost:3333 -i ' + args.private_key + ' ubuntu@' + args.gophish_subdomain + '.' + args.domain], shell=True)

print('You can now access your gophish admin server at https://localhost:3333')


