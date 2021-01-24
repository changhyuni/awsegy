import click
import boto3
import os
import time
import progressbar


### Boto3 Configure
ec2_client = boto3.client('ec2', region_name = 'ap-northeast-2')

### Component Option 
def Search(Search): 
    split_idx = Search.split(':')
    custom_filter = [{'Name':'tag:{}'.format(split_idx[0]), 'Values': ['{}'.format(split_idx[1])]}]
    response = ec2_client.describe_instances(Filters=custom_filter)
    return response['Reservations']

def ProgressBar(Number):
    bar = progressbar.ProgressBar(widgets=[' [', progressbar.Timer(), '] ', progressbar.Bar(), ' (', progressbar.ETA(), ') ',])
    for i in bar(range(Number)):
        time.sleep(0.1)

##############################
#### Main Commnad        #####
##############################
@click.group()
def cli():
    '''
    Interactive CLI tool awsegy \U0001f600
    '''
    pass


@click.command(help='Check your instance information!      ex)"awsegy list tag:Name"')
@click.argument('list')
def list(list):
    try:
        for instance in Search(list):
            print('\nInstance Id : '    + instance['Instances'][0]['InstanceId'])
            print('Publice Ip : '     + instance['Instances'][0]['PublicIpAddress'])
            print('Private Ip : '     + instance['Instances'][0]['PrivateIpAddress'])
            print('Instance State : ' + instance['Instances'][0]['State']['Name']+'\n')
    except:
        print('Oops! There''s no such name.')


@click.command(help='The instance type to change. ex) "awsegy change tag:Name Instance Type")')
@click.argument('change', nargs=2)
def change(change):
    for instance in Search(change[0]):
        ids = []
        id = instance['Instances'][0]['InstanceId']
        ids.append(id)
        if instance['Instances'][0]['State']['Name'] == 'running':
            print(f'Instance Stop Processing : {ids}')
            ec2_client.stop_instances(InstanceIds=ids)
            waiter=ec2_client.get_waiter('instance_stopped')
            ProgressBar(300)
            ec2_client.modify_instance_attribute(InstanceId=id, Attribute='instanceType', Value=change[1])
            ec2_client.start_instances(InstanceIds=ids)
            print(f'Instance Running : {ids}')
        else:
            ec2_client.modify_instance_attribute(InstanceId=id, Attribute='instanceType', Value=change[1])
            ec2_client.start_instances(InstanceIds=ids)
            print(f'Instance Running : {ids}')


@click.command(help='Tagging Instance!        ex)"awsegy tag all tag:Name"')
@click.argument('tag' , nargs=2)
def tag(tag):
    split_idx = tag[1].split(':')
    response = ec2_client.describe_instances()
    instances = response['Reservations']
    instance_ids = []
    if tag[0] == 'all':
        for instance in instances:
            instance_ids.append(instance['Instances'][0]['InstanceId'])
            tage_creation = ec2_client.create_tags(
            Resources = instance_ids, 
            Tags = [{'Key' : f'{split_idx[0]}', 'Value' : f'{split_idx[1]}',}])
            print(f'Finished Instance Count : {len(instance_ids)}')
    else:
        for instance in instances:
            custom_filter = [{'Name':'tag:Name', 'Values': ['{}'.format(tag[0])]}]
            response = ec2_client.describe_instances(Filters=custom_filter)
            instance_ids.append(instance['Instances'][0]['InstanceId'])
            tage_creation = ec2_client.create_tags(
            Resources = instance_ids, 
            Tags = [{'Key' : f'{split_idx[0]}', 'Value' : f'{split_idx[1]}',}])
            print(f'Finished Instance Count : {len(instance_ids)}')
            

        
        
        
@click.command(help='Untagging Instance!        ex)"awsegy dtag all tag:Name"')
@click.argument('dtag' , nargs=2)
def dtag(dtag):
    if dtag[0] == 'all':
        split_idx = dtag[1].split(':')
        response = ec2_client.describe_instances()
        instances = response['Reservations']
        instance_ids = []
        for instance in instances:
            instance_ids.append(instance['Instances'][0]['InstanceId'])
            tage_creation = ec2_client.delete_tags(
            Resources = instance_ids, 
            Tags = [{'Key' : f'{split_idx[0]}', 'Value' : f'{split_idx[1]}',}])
            print(f'Finished Instance Count : {len(instance_ids)}')



def main():
    cli.add_command(list)
    cli.add_command(change)
    cli.add_command(tag)
    cli.add_command(dtag)
    cli()

if __name__ == "__main__":
    main()









