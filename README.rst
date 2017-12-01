.. _Python: http://www.python.org/
.. _PyYAML: http://pyyaml.org/wiki/PyYAML
.. _JMESPath: https://github.com/jmespath/jmespath.py
.. _boto3: https://github.com/boto/boto3

=====
Virga
=====

Virga tests your Cloud resources.

.. raw:: html

    <img src="https://travis-ci.org/gurdulu/virga.svg?branch=master" alt="Travis CI" />
    <a href="https://codeclimate.com/github/gurdulu/virga/maintainability"><img
    src="https://api.codeclimate.com/v1/badges/a8608c689cec6ff7da0f/maintainability" /></a>
    <a href="https://codeclimate.com/github/gurdulu/virga/test_coverage"><img
    src="https://api.codeclimate.com/v1/badges/a8608c689cec6ff7da0f/test_coverage" /></a>

-------------
What is Virga
-------------

From `Wikipedia <https://en.wikipedia.org/wiki/Virga>`_: *"In meteorology, Virga is an observable streak or shaft of
precipitation falling from a cloud that evaporates or sublimates before reaching the ground."*

This piece of software is not about a weather phenomenon. Virga is a tool for analysing your Cloud infrastructure
before the rain catastrophically reaches the ground.

----------------------------------
This project is still in pre-alpha
----------------------------------

There are many things still missing:

* the documentation needs to be completed
* the definition file is just a draft for testing purposes

------------------
Provider supported
------------------

At the moment only `AWS <https://aws.amazon.com/>`_.

------------
Requirements
------------

* Python_
* PyYAML_
* JMESPath_

Specific for AWS
================

* an AWS working account
* boto3_

-----------
Quick start
-----------

1. Install Virga :code:`pip install virga`
2. Create the file ``tests.yaml``
3. :code:`virga-asserts aws tests.yaml`


``tests.yaml`` is the `Tests file`_.

-------
Options
-------

Following the list of options of virga-asserts

.. code:: bash

    usage: virga-asserts [-h] [-d DEFINITIONS] [-l LOGFILE] [-s] [-o OUTPUT] [--debug] {aws} testfile

    positional arguments:
      {aws}                 provider
      testfile              test file

    optional arguments:
      -h, --help            show this help message and exit
      -d DEFINITIONS, --definition DEFINITIONS
                            custom definitions path
      -l LOGFILE, --logfile LOGFILE
                            redirect the output to a log file
      -s, --silent          do not output results
      -o OUTPUT, --output OUTPUT
                            save the resource info into the specified directory
      --debug               show debug

-------------------
Configuration files
-------------------

See `This project is still in pre-alpha`_

There are two types of configuration files.

The (**definitions**) are used for defining the characteristics of the provider and the way we filter the
resources we want to check.

The (**tests**) are specific to the tests we want to implement.

Definitions
===========

The **definitions** describe the way we want to obtain information about a specific resource type.

Each YAML file in the definitions directory is read and assembled into the collective **definitions**.

.. code-block:: yaml

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

.. code-block:: yaml

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


In the configurations above (see `<virga/providers/aws/definitions/subnets.yaml>`_ and
`<virga/providers/aws/definitions/instances.yaml>`_) we declare that for the ``subnets`` section we are going
to instantiate a *client* and invoke an *action* identifying the resources we want to filter with **id** or with
**name**.

The same concept is applied to the ``instances`` section.

The **definitions** are unlikely to be changed as contain information depending on the underlying library (in this
case boto3_).

The default definitions path can be overridden with the option ``--definitions``.

Tests file
==========

An example is worth 1000 words.

You want to know if the subnet with the id ``subnet-0123456789`` has:

* the CIDR block equals to 10.0.0.0/24
* the tag *environment* with the value *staging*

and then you want to know if the EC2 instances with the tag name starting with the value ``my-app`` are in the subnet
``my-subnet``.

.. code:: yaml

    ---
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

The keys *id* and *subnets* are identifiers declared in the definitions file.

The ``assertions`` are the actual tests: each item represents a condition to verify using the query language
JMESPath_. The only exception is the last assertion

.. code:: yaml

    SubnetId=="_lookup('subnets', 'name', 'my-subnet')"

``_lookup`` is not a standard JMESPath construct but a Virga function (see `_lookup function`_).

_lookup function
================

The ``_lookup`` function filters a single resource returning the ID.

In the example above instead of declaring the equality

.. code:: yaml

    SubnetId=="subnet-0123456789"

we have filtered the subnet by the *tag:Name*.

The argument passed to the function are:

* the resource type
* the identifier (eg. *name*)
* the value to search

If no result is found, the test fails.

-----------------
Sample generation
-----------------

See `This project is still in pre-alpha`_

---
FAQ
---

See `This project is still in pre-alpha`_

Recommendation on permissions
=============================

See `This project is still in pre-alpha`_

Why my test is failing
======================

See `This project is still in pre-alpha`_

----------------
Resource mapping
----------------

* `List of AWS resources <docs/resource_mapping_aws.rst>`_

---------------
Advanced topics
---------------

* `Definition file <docs/definition_file.rst>`_
* `How to build a custom provider <docs/custom_provider.rst>`_
