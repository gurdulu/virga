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


## Providers supported

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
2. Create and edit the file `tests.yaml`
3. Launch the command `virga-asserts -p aws -t tests.yaml`

_tests.yaml_ is a [test file](#test-files).


## Configuration files

See [This project is still in pre-alpha](#pre-alpha)

There are two types of configuration files.

The __definitions__ (see [docs/definition_file.md](docs/definition_file.md)) are specific to the provider and define 
the way we want to filter the resources to check. These files are unlikely to be changed.

The __tests__ are the actual tests we want to implement.

<a name="test-files"></a>
### Test files

Let's start with an use case: you want to test that the subnet with the id __subnet-0123456789__ has:

* the CIDR block equals to __10.0.0.0/24__
* the tag __environment__ has value __staging__
* the tag __Name__ has value __my-subnet__

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

The keys __id__ and __name__ are identifiers declared in the definitions file.

The __assertions__ are the actual tests: each item of the list represents a condition to verify using
[JMESPath](https://github.com/jmespath/jmespath.py). 

In the assertions above there is a spurious case

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


## virga-asserts options

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


## Sample generation

Virga comes with a tool for generating test files out of resources.

__virga-samples__ requires:

* a valid provider
* the ID of the resource to exemplify

### Example

The command `virga-assert -p aws -s instances -r i-0123456789` will generate a valid test file for the resource 
__i-0123456789__.

### Options

```text
usage: virga-samples [-h] -p PROVIDER -s SECTION -r RESOURCE [-d DEFINITIONS]

optional arguments:
  -h, --help            show this help message and exit
  -p PROVIDER, --provider PROVIDER
                        provider
  -s SECTION, --section SECTION
                        section
  -r RESOURCE, --resource RESOURCE
                        resource id
  -d DEFINITIONS, --definitions DEFINITIONS
                        definitions path
```

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
