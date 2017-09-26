===============
Definition file
===============

It is a YAML file specific to the provider containing information about the resources to investigate.

Let's start with an example: I want to know the configuration of a subnet knowing only the tag Name.

Using boto3 I would

.. code:: python

    import boto3

    ec2 = boto3.client('ec2')
    result = ec2.describe_subnets(Filters=[{'tag:Name': 'my-subnet'}])

In this few lines of code I can identify a few actions that can be abstracted:

* the filter can be parameterised
* the client can be generic
* the method invoked can be retrieved as attribute

.. code:: python

    import boto3

    client = 'ec2'
    action = 'describe_subnets'
    identifier = 'tag:Name'
    resource_id = 'my-subnet'

    obj = boto3.client(client)
    result = getattr(obj, action)(Filters=[{identifier: resource_id}])

The ``result`` would contain a Python structure like

.. code:: python

    {
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
    }

From the resulting data I want to know the ``SubnetId`` of my subnet.

.. code:: python

    prefix = 'Subnets'
    resource_id = 'SubnetId'
    print(result[prefix][0][resource_id])

Summarising I can identify 6 variables that can be parameterised in an external configuration file.

From the example above the structure of the subnets definition for AWS is:

.. code:: yaml

    subnets:
      client: ec2
      action: describe_subnets
      context: Subnets
      prefix: Subnets
      resource_id: SubnetId
      identifiers:
        id: subnet-id
        name: tag:Name

and for the security groups

.. code:: yaml

    security_groups:
      client: ec2
      action: describe_security_groups
      context: Security Groups
      prefix: SecurityGroups
      resource_id: GroupId
      identifiers:
        id: group-id
        name: tag:Name
        group_name: group-name

The list of identifiers can vary and can be personalised. Our standard definition file can be overridden from the
command line with the option *-definition*.
