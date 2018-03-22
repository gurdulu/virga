# Virga

Virga tests your Cloud resources.

[![Travis CI](https://travis-ci.org/gurdulu/virga.svg?branch=master)](https://travis-ci.org/gurdulu/virga.svg?branch=master)
[![CodeClimate maintainability](https://api.codeclimate.com/v1/badges/a8608c689cec6ff7da0f/maintainability)](https://codeclimate.com/github/gurdulu/virga/maintainability)
[![CodeClimate code coverage](https://api.codeclimate.com/v1/badges/a8608c689cec6ff7da0f/test_coverage)](https://codeclimate.com/github/gurdulu/virga/test_coverage)


## What is Virga

> In meteorology, Virga is an observable streak or shaft of precipitation falling from a cloud that evaporates or 
> sublimates before reaching the ground. <small>[Wikipedia](https://en.wikipedia.org/wiki/Virga)</small>

This piece of software is not about a weather phenomenon. 

Virga is a tool for analysing your Cloud infrastructure before the rain catastrophically reaches the ground.


<a name="pre-alpha"></a>
## This project is still in pre-alpha

There are many things still missing:

* the documentation needs to be completed
* the definition files are just a draft for testing purposes

## Provider supported

At the moment only [AWS](https://aws.amazon.com/).

## Requirements

* [Python](http://www.python.org/)
* [PyYAML](http://pyyaml.org/wiki/PyYAML)
* [JMESPath](https://github.com/jmespath/jmespath.py)

### Specific for AWS

* an AWS working account
* [boto3](https://github.com/boto/boto3)

## Quick start

1. Install Virga `pip install virga`
2. Create the file `tests.yaml`
3. Launch the command `virga-asserts -p aws -t tests.yaml`

_tests.yaml_ is a [test file](#test-files).

## Options

Following the list of options of virga-asserts

```text
usage: virga-asserts [-h] -p {aws} [-t TESTFILE [TESTFILE ...]] [-d DEFINITIONS] [-l LOGFILE] [-s] [-o OUTPUT] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  -p {aws}, --provider {aws}
                        provider
  -t TESTFILE [TESTFILE ...], --testfile TESTFILE [TESTFILE ...]
                        test file
  -d DEFINITIONS, --definitions DEFINITIONS
                        custom definitions path
  -l LOGFILE, --logfile LOGFILE
                        redirect the output to a log file
  -s, --silent          do not output results
  -o OUTPUT, --output OUTPUT
                        save the resource info into the specified directory
  --debug               show debug
```

The command requires a valid provider and at least one test file (see [Test files](#test_files)).

## Configuration files

See [This project is still in pre-alpha](#pre-alpha)

There are two types of configuration files.

The __definitions__ are used for defining the characteristics of the provider and the way we filter the resources 
we want to check.

The __tests__ are specific to the tests we want to implement.

### Definitions

A __definition__ describes the way we want to obtain information about a specific resource type.

Each YAML file in the definitions directory is read and assembled into the collective __definitions__ dictionary then 
used as reference for the tests.

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

In the configurations above (for the actual code see [virga/providers/aws/definitions/subnets.yaml]() and
[virga/providers/aws/definitions/instances.yaml]()) we declare that for the __subnets__ section we are going
to instantiate a _client_ and invoke an _action_ identifying the resources we want to filter with __id__ or with
__name__.

The same concept is applied to the __instances__ section.

The __definitions__ are unlikely to be changed as contain information depending on the underlying library (in this
case [boto3](https://github.com/boto/boto3)).

The default definitions path can be overridden with the option _--definitions_.

<a name="test-files"></a>
### Test files

Let's start with an use case: you want to test that the subnet with the id `subnet-0123456789` has:

* the CIDR block equals to __10.0.0.0/24__
* the tag __environment__ set with the value __staging__

and then you want to know if the EC2 instances with the tag name starting with the value __my-app__ are in the subnet
__my-subnet__.

```yaml
subnets:
- id: subnet-0123456789
  assertions:
  - CidrBlock=='10.0.0.0/24'
  - Tags[?Key=='environment' && Value=='staging']
  - Tags[?Key=='Name' && Value=='my-subnet']
instances:
- name: my-app-*
  assertions:
  - SubnetId=="_lookup('subnets', 'name', 'my-subnet')"
```

The keys __id__ and __subnets__ are identifiers declared in the definitions file.

The __assertions__ are the actual tests: each item represents a condition to verify using the query language
[JMESPath](https://github.com/jmespath/jmespath.py). The only exception is the last assertion

```yaml
SubnetId=="_lookup('subnets', 'name', 'my-subnet')"
```

**_lookup** is not a standard JMESPath construct but a Virga function (see [_lookup function](#lookup-function)).

<a name="lookup-function"></a>
### _lookup function

The **_lookup** function filters a single resource returning the ID.

In the example above instead of declaring the equality

```yaml
SubnetId=="subnet-0123456789"
```

we have filtered the subnet by the __tag:Name__.

The argument passed to the function are:

* the resource type
* the identifier (eg. _name_)
* the value to search

If no result is found, the test fails.

## Sample generation

See [This project is still in pre-alpha](#pre-alpha)

## FAQ

See [This project is still in pre-alpha](#pre-alpha)

### AWS credentials settings

Even if [AWS](https://aws.amazon.com/) requires appropriate credentials, Virga does not explicitly requires any 
credentials setting.

There are several ways to set AWS credentials, if you have some doubts about it, we suggest you to spend some time 
studying this topic before using AWS.

A quick way is using [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

```bash
pip install awscli --upgrade --user
aws configure
```

For more information refer to [boto3 documentation](http://boto3.readthedocs.io/en/latest/guide/configuration.html).

### Why my test is failing

See [This project is still in pre-alpha](#pre-alpha)

## Resource mapping

* [List of AWS resources](docs/resource_mapping_aws.md)

## Advanced topics

* [Definition file](docs/definition_file.md)
* [How to build a custom provider](docs/custom_provider.md)
