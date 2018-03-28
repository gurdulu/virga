# Definition file

A __definition__ describes the way we want to obtain information about a specific resource type.

In other words it is a YAML file containing information about the resources to investigate.

Let's start with an example: I want to know the configuration of a subnet knowing only the tag Name. 

Using boto3 I would:

* create an EC2 client
* invoke the method describe_subnets

```python
import boto3

ec2 = boto3.client('ec2')
result = ec2.describe_subnets(Filters=[{'tag:Name': 'my-subnet'}])
```

In this few lines of code I can identify a few variables:

* the filter (key and value)
* the client 
* the method invoked

```python
import boto3

client = 'ec2'
action = 'describe_subnets'
identifier = 'tag:Name'
resource_id = 'my-subnet'

obj = boto3.client(client)
result = getattr(obj, action)(Filters=[{identifier: resource_id}])
```

The __result__ would contain a Python structure like

```python
result = {
    'ResponseMetadata': {
        'HTTPHeaders': {
            'content-type': 'text/xml;charset=UTF-8',
            'date': 'Wed, 20 Sep 2017 17:25:32 GMT',
            'server': 'AmazonEC2',
            'transfer-encoding': 'chunked',
            'vary': 'Accept-Encoding'
        },
        'HTTPStatusCode': 200,
        'RequestId': '4b1fdfcf-68f9-4f92-95c1-c5f7528f03f6',
        'RetryAttempts': 0
    },
    'Subnets': [
        {
            'AssignIpv6AddressOnCreation': False,
            'AvailabilityZone': 'eu-west-2a',
            'AvailableIpAddressCount': 251,
            'CidrBlock': '172.0.0.0/24',
            'DefaultForAz': False,
            'Ipv6CidrBlockAssociationSet': [],
            'MapPublicIpOnLaunch': False,
            'State': 'available',
            'SubnetId': 'subnet-01234567',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'my-subnet'
                },
                {
                    'Key': 'environment',
                    'Value': 'staging'
                }
            ],
            'VpcId': 'vpc-01234567'
        }
    ]
}
```

From the resulting data I want to know the __SubnetId__ of the subnet found.

```python
import boto3

client = 'ec2'
action = 'describe_subnets'
identifier = 'tag:Name'
resource_id = 'my-subnet'

prefix = 'Subnets'
resource_id = 'SubnetId'

obj = boto3.client(client)
result = getattr(obj, action)(Filters=[{identifier: resource_id}])

print(result[prefix][0][resource_id])
```

Summarising I can identify 6 variables that can be set as parameters in an external configuration file.

From the example above the structure of the subnets definition for AWS is:

```yaml
subnets:
  client: ec2
  action: describe_subnets
  context: Subnets
  prefix: Subnets
  resource_id: SubnetId
  identifiers:
    id: 
      key: subnet-id
      type: filter
    name: 
      key: tag:Name
      type: filter
```

I can replicate the same structure for security groups

```yaml
security_groups:
  client: ec2
  action: describe_security_groups
  context: Security Groups
  prefix: SecurityGroups
  resource_id: GroupId
  identifiers:
    id: 
      key: group-id
      type: filter
    name: 
      key: tag:Name
      type: filter      
    group_name: 
      key: group-name
      type: filter
```

and EC2 instances

```yaml
instances:
  client: ec2
  action: describe_instances
  context: EC2 Instances
  prefix: Reservations.Instances
  resource_id: InstanceId
  identifiers:
    id:
      key: instance-id
      type: filter
    name:
      key: tag:Name
      type: filter
```

The code is at [virga/providers/aws/definitions/]().

## Definitions directory

The __definitions__ are unlikely to be changed as they contain information depending on the underlying library (in 
this case [boto3](https://github.com/boto/boto3)).

The list of identifiers can vary and can be personalised. Our standard definition files can be overridden from the
command line with the option **--definitions**.

Each YAML file in the definitions directory is read and assembled into the collective __definitions__ dictionary then 
used as reference for the tests.
