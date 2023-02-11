# autosneakphish
Automated evasive phishing infrastructure

The goal of autosneakphish is to enable rapid deployment of phishing infrastructure that is capable of evading email security controls.
To that end autosneakphish utilizes GoPhish in conjunction with AWS SES. The automation is performed by terraform and ansible.
A python script performs most of the heavy lifting and ensure that not only does it perform its functions the first time
it also can be ran multiple times without the need for a new clone of the repository.

Autosneakphish will configure your phishing site to utilize https and obtain a certificate automatically.
After autosneakphish.py runs succesfully you will be able to access GoPhish immediately in your browser.

## Software Dependencies

- awscli 
- terraform
- ansible
- python3

## Configuration

- You must create aws-cli keys and run aws configure to add them to your awscli environment.
- Your aws user must have the permissions to manage EC2, SES, Route53, and IAM.
- You need to create a EC2 key pair and download it the autopsneakphish directory.
- Aquire a domain and create a hosted zone in aws - you will need the domain name and the hosted zone id to run autosneakphish.py
- Your SES account must be in production https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html
- You need to modify the profile value in main.tf with the correct profile for your aws cli keys
- Ensure that you choose an ubuntu image for the AMI replacement in the variables.tf file

## Installation

- git clone https://github.com/WhiteOakSecurity/autosneakphish.git
- Creat aws-cli keys and add them to your awscli configuration using "aws configure"  
- chmod +x autosneakphish.py

To obtain ses smtp username to input into gophish profile run the following command after running autosneakphish.py.

- rg unique_id terraform.tfstate

To obtain ses stmp password to input into gophish profile run the following command after running autosneakphish.py.

- rg ses_smtp_password_v4 terraform.tfstate | tail -n 1

## Usage

```
usage: autosneakphish.py [-h] [-s SERVERSTRING] [-r RID_REPLACE] -d DOMAIN -g GOPHISH_SUBDOMAIN [-m MX_SUBDOMAIN] -a AMISTRING -p PRIVATE_KEY -w WHITELIST_CIDR -z ZONE_ID -v VPC_ID -t TITLE -b BODY

Automated evasive phishing infrastructure tool.

options:
  -h, --help            show this help message and exit
  -s SERVERSTRING, --serverstring SERVERSTRING
                        Your Servername and Header replacement string
  -r RID_REPLACE, --rid_replace RID_REPLACE
                        Your rid parameter replacement string
  -d DOMAIN, --domain DOMAIN
                        Your SMTP sending domain name
  -g GOPHISH_SUBDOMAIN, --gophish_subdomain GOPHISH_SUBDOMAIN
                        Your GoPhish landing page sub-domain
  -m MX_SUBDOMAIN, --mx_subdomain MX_SUBDOMAIN
                        Your MX sub-domain
  -a AMISTRING, --amistring AMISTRING
                        Your ami
  -p PRIVATE_KEY, --private_key PRIVATE_KEY
                        Your aws private key
  -w WHITELIST_CIDR, --whitelist_cidr WHITELIST_CIDR
                        Your Public IP address for connecting to infrastructure
  -z ZONE_ID, --zone_id ZONE_ID
                        Your AWS zone_id
  -v VPC_ID, --vpc_id VPC_ID
                        Your AWS vpc id
  -t TITLE, --title TITLE
                        Customize your 404 file Title
  -b BODY, --body BODY  
                        Customize your 404 file text
                      
 ```

 ```
 ./autosneakphish.py -s optionalserverstring -r optionalridstring -d requireddomain.com -g optionalsubdomain -m optionalmxsubdomain -a ami-youramihere -p yourprivatekey.pem -w yourIP/32 -z yourhostedzoneid -v vpc-yourvpcid -t title -b body
 
```

