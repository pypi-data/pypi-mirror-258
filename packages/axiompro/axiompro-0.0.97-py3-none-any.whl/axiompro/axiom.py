#!/usr/bin/env python3

import argparse
import base64
import json
import boto3
import datetime
import paramiko
import botocore
import os
import time
from tabulate import tabulate
from rich.progress import track
from rich.console import Console
from rich import print as rprint
import rich
from botocore.exceptions import ClientError
from concurrent.futures import ThreadPoolExecutor
import threading 
from paramiko.util import deflate_long
import struct
import base64

console = Console()
def get_axiom_dir():
    home_dir = os.path.expanduser('~')

    return f"{home_dir}/.axiom"

def save_config(config):
    axiom_dir = get_axiom_dir()
    config_path = f'{axiom_dir}/config.json'
    profiles = f'{axiom_dir}/profiles'
    os.makedirs(profiles, exist_ok=True)
    profiles_path = f'{profiles}/{config["profile"]}.json'
    with open(profiles_path, 'w+') as f:
        f.write(json.dumps(config, indent=4))
        f.close()

    with open(config_path, 'w') as f:
        f.write(json.dumps(config, indent=4))
        f.close()

def switch_profile(profile):
    axiom_dir = get_axiom_dir()
    config_path = f'{axiom_dir}/config.json'
    profiles = f'{axiom_dir}/profiles'
    profiles_path = f'{profiles}/{profile}.json'
    with open(profiles_path, 'r') as f:
        config = json.loads(f.read())
        f.close()

    with open(config_path, 'w') as f:
        f.write(json.dumps(config, indent=4))
        f.close()


def configure(user_config=False):
    prompts = [
        {
            "variable": "profile",
            "prompt": "Enter a profile name",
            "default": "axiom",
            "required": True
        },
        {
            "variable": "instance_type",
            "prompt": "Enter an instance type",
            "default": "t3.micro",
            "required": True
        },
        {
            "variable": "AWS_ACCESS_KEY_ID",
            "prompt": "Enter your AWS_ACCESS_KEY_ID",
            "default": "",
            "required": True
        },
        {
            "variable": "AWS_SECRET_ACCESS_KEY",
            "prompt": "Enter your AWS_SECRET_ACCESS_KEY",
            "default": "",
            "required": True
        },
        {
            "variable": "AWS_DEFAULT_REGION",
            "prompt": "Enter your AWS_DEFAULT_REGION",
            "default": "us-west-2",
            "required": True
        }
    ]

    config = {}
    for prompt in prompts:
        ok = False
        while not ok:
            if prompt["variable"] in user_config:
                prompt["default"] = user_config[prompt["variable"]]

            config[prompt["variable"]] = input(f'{prompt["prompt"]} (default: {prompt["default"]}): ') or prompt["default"]

            if config[prompt["variable"]] == "" and prompt["required"]:
                print(f"Error: {prompt['variable']} is required")
            else:
                ok = True

    save_config(config)
    return config

def list_profiles():
    axiom_dir = get_axiom_dir()
    profiles = f'{axiom_dir}/profiles'
    profiles_list = os.listdir(profiles)
    return profiles_list

def print_profiles():
    profiles = list_profiles()
    console.print(profiles)

def delete_profile(profile):
    axiom_dir = get_axiom_dir()
    profiles = f'{axiom_dir}/profiles'
    profiles_path = f'{profiles}/{profile}.json'
    os.remove(profiles_path)

def get_config():
    axiom_dir = get_axiom_dir()
    if not os.path.exists(axiom_dir) or not os.path.exists(f"{axiom_dir}/config.json"):
        console.print(f"- Creating directory for configuration...", style="bold white", highlight=False)
        os.makedirs(axiom_dir, exist_ok=True)
        os.makedirs(f"{axiom_dir}/keys", exist_ok=True)
        console.print(f"- Directory created successfully", style="bold white", highlight=False)

        configure()

    with open(f"{axiom_dir}/config.json", "r") as f:
        config = json.loads(f.read())

    return config

config = get_config()

if config["AWS_ACCESS_KEY_ID"] and config["AWS_SECRET_ACCESS_KEY"] and config["AWS_DEFAULT_REGION"]:
    ec2 = boto3.client('ec2', aws_access_key_id=config["AWS_ACCESS_KEY_ID"], aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"], region_name=config["AWS_DEFAULT_REGION"])
else:
    ec2 = boto3.client('ec2')

def get_ubuntu_image():
    query_str = f'ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server*'
    images = ec2.describe_images(Filters=[{'Name':'name', 'Values':[query_str]}])
    clean = []
    for image in images["Images"]:
        if "amazon/ubuntu/images/hvm-ssd" in image["ImageLocation"]:
            clean.append(image)

    latest_image = clean[-1]
    return latest_image

config["image_id"] = get_ubuntu_image()["ImageId"]
save_config(config)

def create_security_group(name):
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2.create_security_group(GroupName=name, Description=f'{name} security group', VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
        return security_group_id
    except ClientError as e:
        response = ec2.describe_security_groups(
            Filters=[
            dict(Name='group-name', Values=[name])
            ]
        )
        group_id = response['SecurityGroups'][0]['GroupId']
        return group_id

def list_local_key_pairs():
    axiom_dir = get_axiom_dir()
    keys_dir = f"{axiom_dir}/keys"
    keypairs = os.listdir(keys_dir)
    return keypairs

def pubkey_from_privatekey(private_key_material):
    key = paramiko.RSAKey.from_private_key_file(private_key_material)
    output = b''
    parts = [b'ssh-rsa', deflate_long(key.public_numbers.e), deflate_long(key.public_numbers.n)]
    for part in parts:
        output += struct.pack('>I', len(part)) + part
    public_key = b'ssh-rsa ' + base64.b64encode(output) + b'\n'
    return public_key

def create_key_pair(keypair_name):
    try:
        axiom_dir = get_axiom_dir()
        # if keypair exists locally, upload it, else create it
        local_keypairs = list_local_key_pairs()
        aws_keypairs = list_key_pairs()['KeyPairs']

        if f"{keypair_name}.pem" in local_keypairs and keypair_name not in [keypair['KeyName'] for keypair in aws_keypairs]:
            with open(f"{axiom_dir}/keys/{keypair_name}.pem", "r") as f:
                private_key = f.read()
                public_key = pubkey_from_privatekey(f"{axiom_dir}/keys/{keypair_name}.pem")

                response = ec2.import_key_pair(KeyName=keypair_name, PublicKeyMaterial=public_key)

        # else in case exists in local aws but not in local, delete it, regenerate and upload 
        elif keypair_name in [keypair['KeyName'] for keypair in aws_keypairs] and f"{keypair_name}.pem" not in local_keypairs:
            response = delete_key_pair(keypair_name)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(f"Key pair {keypair_name} deleted successfully")
                key_pair = ec2.create_key_pair(KeyName=keypair_name)

                private_key = key_pair["KeyMaterial"]
                axiom_dir = get_axiom_dir()
                key_path = f"{axiom_dir}/keys/{keypair_name}.pem"
                with os.fdopen(os.open(key_path, os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
                    handle.write(private_key)
        # else if it exists in neither, create it
        elif keypair_name not in [keypair['KeyName'] for keypair in aws_keypairs] and f"{keypair_name}.pem" not in local_keypairs:
            key_pair = ec2.create_key_pair(KeyName=keypair_name)

            private_key = key_pair["KeyMaterial"]
            axiom_dir = get_axiom_dir()
            key_path = f"{axiom_dir}/keys/{keypair_name}.pem"
            with os.fdopen(os.open(key_path, os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
                handle.write(private_key)
        elif keypair_name in [keypair['KeyName'] for keypair in aws_keypairs] and f"{keypair_name}.pem" in local_keypairs:
            #print(f"Key pair {keypair_name} already exists")
            return keypair_name
        
    except Exception as e:
        print(str(e))

    return keypair_name

def create_instance(instance_name, instance_type, image_id, security_group_id, keypair_name, profile):
    response = ec2.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {

                    'DeleteOnTermination': True,
                    'VolumeSize': 8,
                    'VolumeType': 'gp2'
                },
            },
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name','Value': instance_name}, {'Key':'Profile', 'Value':profile}],
            }
        ],
        ImageId=image_id,
        KeyName=keypair_name,
        InstanceType=instance_type,
        MaxCount=1,
        MinCount=1,
        Monitoring={
            'Enabled': False
        },
        SecurityGroupIds=[
            security_group_id
        ],
    )

    return response

## function to attempt to connect to an instance and loop until it is available
def test_ssh(instance_name):
    for instance in get_instances_minimal():
        if instance['name'] == instance_name:
            public_ip = instance['publicIpAddress']
            profile = instance['profile']
            axiom_dir = get_axiom_dir()
            pkey = paramiko.RSAKey.from_private_key_file(f"{axiom_dir}/keys/{profile}.pem")

            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(public_ip, username="ubuntu", pkey=pkey)
                client.close()
                return True
            except Exception as e:
                return False
            
def test_ssh_loop(instance_name):
    while True:
        if test_ssh(instance_name):
            break
        else:
            time.sleep(5)

def create_base_instance(instance_name, instance_type, profile_name, build_name):

    security_group_id = create_security_group(profile_name)
    keypair_name = create_key_pair(profile_name)
    
    latest_ubuntu_ami = get_ubuntu_image()["ImageId"]
    console.print(f"==> Creating instance: {instance_name}", style="bold white", highlight=False)
    resp = create_instance(instance_name, instance_type, latest_ubuntu_ami, security_group_id, keypair_name, profile_name)

    # check until instance is initialized
    
    with rich.progress.Progress(rich.progress.SpinnerColumn(), transient=True, auto_refresh=True) as progress:
        console.print("==> Waiting for instance to initialize...", style="bold white", highlight=False)
        task_id = progress.add_task("Waiting for instance to initialize...", total=100)
        
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[resp['Instances'][0]['InstanceId']])
        console.print(f"==> Instance {instance_name} running, attempting to connect...", style="bold white", highlight=False)
        test_ssh_loop(instance_name)
        public_ip = ec2.describe_instances(InstanceIds=[resp['Instances'][0]['InstanceId']])['Reservations'][0]['Instances'][0]['PublicIpAddress']
        console.print(f"==> Instance {instance_name} accessible at {public_ip}", style="bold white")
        time.sleep(2)
        progress.update(task_id, completed=100)

        console.print("")
        time.sleep(1)

    with rich.progress.Progress(rich.progress.BarColumn(), rich.progress.TimeElapsedColumn(), transient=True, auto_refresh=True) as progress:
        code = """sudo apt update
sudo apt-get upgrade -y
sudo apt-get install -y zsh
sudo chsh -s $(which zsh) ubuntu
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
wget -q -O - https://archive.kali.org/archive-key.asc | sudo apt-key add -
sudo sh -c "echo 'deb https://http.kali.org/kali kali-rolling main non-free contrib' > /etc/apt/sources.list.d/kali.list"
sudo sh -c "echo 'Package: *' > /etc/apt/preferences.d/kali.pref; echo 'Pin: release a=kali-rolling' >> /etc/apt/preferences.d/kali.pref; echo 'Pin-Priority: 50' >> /etc/apt/preferences.d/kali.pref"
wget http://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2022.1_all.deb
sudo dpkg -i kali-archive-keyring_2022.1_all.deb
rm kali-archive-keyring_2022.1_all.deb
sudo apt update
sudo apt update --fix-missing
sudo apt install -f
sudo apt --fix-broken install
sudo apt -y upgrade
sudo apt -y install ffuf nmap subfinder httpx-toolkit nuclei wordlists amass gobuster"""

        length = len(code.split("\n")) + 4

        task_id = progress.add_task("Configuring instance...", total=length)

        for idx, line in enumerate(code.split("\n")):
            if line == "":
                continue
            
            console.print()
            progress.update(task_id, completed=idx + 1)
            ssh_exec(instance_name, line, progress)

        console.print("")

        time.sleep(15)
        progress.update(task_id, completed=length)

        completed = length

        progress.console.print(f"==> Creating image: {profile_name}-{build_name}", style="bold white", highlight=False)
        completed += 1
        progress.update(task_id, completed=completed)
        resp = ec2.create_image(InstanceId=resp['Instances'][0]['InstanceId'], Name=build_name, NoReboot=True)
       
        completed += 1
        progress.console.print(f"==> Waiting for image to be available...", style="bold white")
        progress.update(task_id, completed=completed)
        waiter = ec2.get_waiter('image_available')
        waiter.wait(Filters=[{'Name': 'image-id', 'Values': [resp["ImageId"]]}])

        progress.console.print(f"==> Image {build_name} created successfully", style="bold white", highlight=False)
        progress.console.print(f"==> Cleaning up instance {instance_name}", style="bold white", highlight=False)
        completed += 1
        progress.update(task_id, completed=completed)

        config["image_id"] = resp["ImageId"]
        save_config(config)
    
        delete_instances(instance_names=[instance_name])
        progress.console.print(f"==> Instance {instance_name} deleted successfully", style="bold white", highlight=False)
        completed += 1
        progress.console.print(f"==> Image {profile_name}-{build_name} created successfully", style="bold white", highlight=False)
        progress.update(task_id, completed=completed)

    return resp

def snapshot(instance_id, build_name):
    resp = ec2.create_image(InstanceId=instance_id, Name=build_name, NoReboot=True)
    print(resp)




def init_instance(instance_name, instance_type, profile_name, source_image_id):
    security_group_id = create_security_group(profile_name)
    keypair_name = create_key_pair(profile_name)
    resp = create_instance(instance_name, instance_type, source_image_id, security_group_id, keypair_name, profile_name)
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[resp['Instances'][0]['InstanceId']])
    console.print(f"==> Instance {instance_name} initialized successfully...", style="bold white")
    test_ssh_loop(instance_name)

def extract_info(reservation):
    clean = {
        'instanceId': reservation['Instances'][0]['InstanceId'],
        'instanceType': reservation['Instances'][0]['InstanceType'],
        'architecture': reservation['Instances'][0]['Architecture'],
        'currentStatus': reservation['Instances'][0]['State']['Name'],
        'name':None
    }

    try:
        clean['tags'] = reservation['Instances'][0]['Tags']
        clean['privateIpAddress'] = reservation['Instances'][0]['PrivateIpAddress']
        clean['publicIpAddress'] = reservation['Instances'][0]['PublicIpAddress']
        clean['publicDnsName'] = reservation['Instances'][0]['PublicDnsName']
        clean['privateDnsName'] = reservation['Instances'][0]['PrivateDnsName']

        name_tag = [tag['Value'] for tag in clean['tags'] if tag['Key'] == 'Name']
        profile_tag = [tag['Value'] for tag in clean['tags'] if tag['Key'] == 'Profile']
        clean['name'] = name_tag[0]
        clean['profile'] = profile_tag[0]
    except:
        pass

    return clean


def get_images():
    images = ec2.describe_images(Owners=['self'])
    
    return images

def print_images():
    images = get_images()['Images']

    images_minimal = []
    for image in images:
        image_meta = [
            image['ImageId'],
            image['ImageLocation'],
            image['CreationDate']
        ]

        images_minimal.append(image_meta)
    
    print(tabulate(images_minimal, headers=["ID", "Location", "Date"], tablefmt='grid'))

def get_instances(instance_ids=[]):
    if len(instance_ids) > 0:
        return(ec2.describe_instances(InstanceIds=instance_ids))
    else:
        return(ec2.describe_instances())

def get_instances_minimal(instance_ids=[]):
    instances = get_instances(instance_ids)

    clean_instances = []
    for res in instances["Reservations"]:
        clean = extract_info(res)
        if clean['currentStatus'] != 'terminated':
            clean_instances.append(clean)

    return clean_instances


def format_table(data):
    headers = ['Name', 'Instance ID', 'Instance Type', 'Status', 'Private IP', 'Public IP', 'Public DNS']
    
    # Extract the values for tags and name from the data
    tags_column = [format_tags_and_name(instance['tags'], instance['name']) for instance in data]
    

    # Re-format the data to include the tags and name columns
    reformatted_data = [[tags_column[i][1],
        instance['instanceId'],
        instance['instanceType'], 
                    instance['currentStatus'],
                    instance.get('privateIpAddress', 'N/A'),
                    instance.get('publicIpAddress', 'N/A'),
                    instance.get('publicDnsName', 'N/A')] 
                    for i, instance in enumerate(data)]
    
    return tabulate(reformatted_data, headers, tablefmt='grid')

# Define a function to format the tags and instance name
def format_tags_and_name(tags, name):
    if tags:
        tag_str = ', '.join(['{}: {}'.format(tag['Key'], tag['Value']) for tag in tags])
    else:
        tag_str = 'N/A'

    if name:
        name_str = name
    else:
        name_str = 'None'

    return tag_str, name_str

def print_instances():
    instances = get_instances_minimal()

    print(format_table(instances))

def ssh_to_instance(instance_name):
    for instance in get_instances_minimal():
        if instance['name'] == instance_name:
            public_ip = instance['publicIpAddress']
            profile = instance['profile']

            axiom_dir = get_axiom_dir()
            os.system(f"ssh -i {axiom_dir}/keys/{profile}.pem ubuntu@{public_ip}")

# function to delete ami by ami id
def delete_ami(ami_id):
    try:
        ec2.deregister_image(ImageId=ami_id)
        print(f"AMI {ami_id} deleted successfully")
    except Exception as e:
        print(f"Error deleting AMI {ami_id}: {e}")

def list_key_pairs():
    response = ec2.describe_key_pairs()
    return response

def delete_key_pair(keypair_name):
    response = ec2.delete_key_pair(KeyName=keypair_name)
    return response

def print_keypair_delete(keypair_name):
    response = delete_key_pair(keypair_name)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Key pair {keypair_name} deleted successfully")
    else:
        print(f"Error deleting key pair {keypair_name}")


def print_keypairs():
    keypairs = list_key_pairs()['KeyPairs']
    keypairs_minimal = []
    for keypair in keypairs:
        keypair_meta = [
            keypair['KeyName'],
            keypair['KeyFingerprint']
        ]

        keypairs_minimal.append(keypair_meta)
    
    print(tabulate(keypairs_minimal, headers=["Name", "Fingerprint"], tablefmt='grid'))

def upload_keypair(keypair_name, private_key_file):
    try:
        key = paramiko.RSAKey.from_private_key_file(private_key_file)
        output = b''
        parts = [b'ssh-rsa', deflate_long(key.public_numbers.e), deflate_long(key.public_numbers.n)]
        for part in parts:
            output += struct.pack('>I', len(part)) + part
        public_key = b'ssh-rsa ' + base64.b64encode(output) + b'\n'
        
        response = ec2.import_key_pair(KeyName=keypair_name, PublicKeyMaterial=public_key)
        print(f"Key pair {keypair_name} uploaded successfully")
    except Exception as e:
        print(f"Error uploading key pair {keypair_name}: {e}")

def ssh_exec(instance_name, code, progress):
    output = ""
    progress.console.print(f"==> Executing: {code} on {instance_name}", style="bold white", highlight=False)

    for instance in get_instances_minimal():
        if instance['name'] == instance_name:
            public_ip = instance['publicIpAddress']
            profile = instance['profile']
            axiom_dir = get_axiom_dir()
            pkey = paramiko.RSAKey.from_private_key_file(f"{axiom_dir}/keys/{profile}.pem")

            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(public_ip, username="ubuntu", pkey=pkey)
            _stdin, _stdout,_stderr = client.exec_command(code)
            _stdin.close()
            for line in iter(lambda: _stdout.readline(1024), ""):
                if line != "":
                    progress.console.print(line, end="", style="blue", highlight=False)
            client.close()

def delete_instances(instance_names=[]):
    instances = get_instances_minimal()
    ids_to_be_deleted = []

    for instance_name in instance_names:
        for instance in instances:
            if instance['name'] == instance_name:
                ids_to_be_deleted.append(instance['instanceId'])

    resp = ec2.terminate_instances(
        InstanceIds = ids_to_be_deleted,
        DryRun=False
    )

parser = argparse.ArgumentParser(description='axiom Instance Orchestration')

# Instance Management

parser.add_argument('--configure', action='store_true',
                    help='Configure axiom')

parser.add_argument('--build', action='store_true',
                    help='Build a new base AWS instance')

parser.add_argument('--build-script',  
                    help='Optional bash script to supply with --build, will append to the default build process')

parser.add_argument('instance_name', nargs='?',
                    help='Name of the instance to perform an operation for')

parser.add_argument('--instance-type', default='t3.micro',
                    help='Type of the instance (default: t3.micro)')
parser.add_argument('--profile', default=config["profile"],
                    help=f'Profile of the instance (default: {config["profile"]})')

# select profile
parser.add_argument('--select-profile', 
                    help='Profile to use')

# list profiles
parser.add_argument('--profiles', action='store_true',
                    help='List profiles')

# get current config
parser.add_argument('--get-config', action='store_true',
                    help='Get current config')

# delete profile
parser.add_argument('--rm-profile', 
                    help='Profile to delete')

parser.add_argument('--prefix', 
                    help='Prefix of the fleet')

# Fleet Initialization
parser.add_argument('--init', 
                    help='Initialize a new fleet of instances')
parser.add_argument('-n', type=int, default=1,
                    help='Number of nodes to initialize (default: 1)')

parser.add_argument('--images', action='store_true',
                    help='Print a table of images')

parser.add_argument('--image-id', default=config["image_id"], 
                    help='Image ID to use as the base image')

parser.add_argument('--rm-image', 
                    help='Image ID/s to delete', nargs='+')

parser.add_argument('--keypairs', action='store_true',
                    help='List keypairs')

parser.add_argument('--rm-keypair', 
                    help='Key pair/s to delete', nargs='+')

parser.add_argument('--upload-keypair', action='store_true',
                    help='Upload a keypair to AWS')

parser.add_argument('--keypair-private-key',
                    help='Public key file to upload')

parser.add_argument('--keypair-name',
                    help='Name of the keypair to upload')

# Snapshot
parser.add_argument('--snapshot', 
                    help='Snapshot an instance by name to create an iamge')

# Instance Interaction
parser.add_argument('--instances', action='store_true',
                    help='Print a table of instance information')
parser.add_argument('--ssh',
                    help='Interactively SSH into an instance')

parser.add_argument('--exec',
                    help='Execute a single command over SSH')

parser.add_argument('--rm', nargs='*', default=[], action='store',
                    help='List of instance names to delete')

def main():

    intro = """
 ▄▄▄      ▒██   ██▒ ██▓ ▒█████   ███▄ ▄███▓    ██▓███   ██▀███   ▒█████  
▒████▄    ▒▒ █ █ ▒░▓██▒▒██▒  ██▒▓██▒▀█▀ ██▒   ▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒
▒██  ▀█▄  ░░  █   ░▒██▒▒██░  ██▒▓██    ▓██░   ▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒
░██▄▄▄▄██  ░ █ █ ▒ ░██░▒██   ██░▒██    ▒██    ▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░
 ▓█   ▓██▒▒██▒ ▒██▒░██░░ ████▓▒░▒██▒   ░██▒   ▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░
 ▒▒   ▓▒█░▒▒ ░ ░▓ ░░▓  ░ ▒░▒░▒░ ░ ▒░   ░  ░   ▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░ 
  ▒   ▒▒ ░░░   ░▒ ░ ▒ ░  ░ ▒ ▒░ ░  ░      ░   ░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░ 
  ░   ▒    ░    ░   ▒ ░░ ░ ░ ▒  ░      ░      ░░         ░░   ░ ░ ░ ░ ▒  
      ░  ░ ░    ░   ░      ░ ░         ░                  ░         ░ ░  
                          author: pry0cc
    """

    console.print(intro)

    args = parser.parse_args()
    # Validate arguments for exclusivity
    if (args.build and args.rm) or \
        (args.init and args.rm) or \
        (args.init and args.build) or \
        (args.ssh and args.rm) or \
        (args.ssh and args.instances):
        parser.error("Invalid combination of arguments. "
                 "Choose only one of: --build, --init, --rm, --ssh, --instances.")


    if args.select_profile:
        switch_profile(args.select_profile)

    if args.configure:
        console.print("==> Configuring axiom...", style="bold white")
        print(configure(user_config=config))
        console.print("==> Configuration saved", style="bold white")

    if args.profiles:
        print_profiles()

    if args.rm_profile:
        console.print(f"==> Deleting profile: {args.rm_profile}", style="bold white")
        delete_profile(args.rm_profile)

    if args.get_config:
        print(get_config())

    # Build instance
    if args.build:
        build_name = ""
        if args.instance_name:
            build_name = args.instance_name
        else:
            build_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

        create_base_instance(f'{args.profile}-{build_name}', args.instance_type, args.profile, build_name)


    if args.upload_keypair:
        if args.keypair_private_key and args.keypair_name:
            upload_keypair(args.keypair_name, args.keypair_private_key)
        else:
            print("Please supply arguments: --keypair-private-key and --keypair-name")

    # Initialize fleet
    if args.init:
        num_nodes = args.n
        prefix = args.init

        #print(f'Initializing a fleet with {num_nodes} node/s.')
        console.print(f'==> Initializing a fleet named {prefix} with {num_nodes} node/s.', style="bold white")

        # Function to run in thread
        def init_instance_threaded(i):
            instance_name = f'{prefix}{i}'
            instance_type = 't3.micro' 
            profile_name = args.profile
            source_image_id = args.image_id
            init_instance(instance_name, instance_type, profile_name, source_image_id)
            # loop until instance is initialized
            public_ip = ec2.describe_instances(Filters=[{'Name':'tag:Name', 'Values':[instance_name]}])['Reservations'][0]['Instances'][0]['PublicIpAddress']
            console.print(f"==> Instance {instance_name} initialized successfully at {public_ip}", style="bold white")

        # Use ThreadPoolExecutor to run threads
        with ThreadPoolExecutor(max_workers=num_nodes) as executor:
            futures = [executor.submit(init_instance_threaded, i) for i in range(num_nodes)]
        
        # Wait for threads to complete
        for future in futures:
            future.result() 

        console.print("All instances initialized", style="bold white")

    if args.snapshot:
        instance_id = args.snapshot
        base_image = args.image_id
        snapshot(instance_id, base_image)

    if args.rm_image:
        for image_id in args.rm_image:
            delete_ami(image_id)

    # Print instances
    if args.instances:
        print_instances()

    if args.images:
        print_images()

    # SSH into instance
    if args.ssh:
        ssh_to_instance(args.ssh)


    if args.exec:
        with rich.progress.Progress(rich.progress.SpinnerColumn(), transient=True, auto_refresh=True) as progress:
            if args.prefix:
                instances = []
                instances_minimal = get_instances_minimal()
                task_id = progress.add_task("Executing command on instances...", total=len(instances_minimal))
                for idx, instance in enumerate(instances_minimal):
                    
                    if instance["name"].startswith(args.prefix):
                        instances.append(instance["name"])

                with ThreadPoolExecutor(max_workers=len(instances)) as executor:
                    futures = [executor.submit(ssh_exec, instance, args.exec, progress) for instance in instances]

                for future in futures:
                    future.result()
            else:
                ssh_exec(args.instance_name, args.exec, progress)

    if args.keypairs:
        print_keypairs()

    if args.rm_keypair:
        for keypair in args.rm_keypair:
            print_keypair_delete(keypair)

    if args.rm:
        if args.prefix:
            print(f'Deleting instances with prefix: {args.prefix}')
            instances = []
            for instance in get_instances_minimal():
                if instance["name"].startswith(args.prefix):
                    instances.append(instance["name"])
            delete_instances(instances)
        else:
            print(f'Deleting specific instances: {", ".join(args.rm)}')
            delete_instances(args.rm)


if __name__ == "__main__":
    # capture ctrl+c and exit gracefully
    try:
        main()
    except KeyboardInterrupt:
        console.print("")
        console.print("Exiting...")