.. _Python: http://www.python.org/
.. _PyYAML: http://pyyaml.org/wiki/PyYAML
.. _JMESPath: https://github.com/jmespath/jmespath.py
.. _boto3: https://github.com/boto/boto3

=====
Virga
=====

Virga tests your Cloud resources.

-------------
What is Virga
-------------

From `Wikipedia <https://en.wikipedia.org/wiki/Virga>`_: *"In meteorology, Virga is an observable streak or shaft of
precipitation falling from a cloud that evaporates or sublimates before reaching the ground."*

This piece of software is not about a weather phenomenon. In this context Virga is a tool for analysing your Cloud
infrastructure before the rain reaches the ground.

----------------------------------
This project is still in pre-alpha
----------------------------------

There are many things still missing:

* the documentation needs to be completed
* the definition file is just a draft for testing purposes
* it needs tests on real data resources

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
2. Edit the file ``template.yaml``
3. :code:`virga template.yaml`


``template.yaml`` is the `Configuration files`_.

-------
Options
-------

See `This project is still in pre-alpha`_

-------------------
Configuration files
-------------------

See `This project is still in pre-alpha`_

There are two types of configuration files.

The first one (**definitions**) is used for defining the characteristics of the provider and the way we filter the
resources we want to check.

The second one (**tests**) is specific to the tests we want to implement.

Definitions
===========

The **definitions** describe the way we want to obtain information about a specific resource type

.. code-block::yaml

    subnets:
      client: ec2
      action: describe_subnets
      context: Subnets
      prefix: Subnets
      resource_id: SubnetId
      identifiers:
        id: subnet-id
        name: tag:Name
    instances:
      client: ec2
      action: describe_instances
      context: EC2 Instances
      prefix: Reservations.Instances
      resource_id: InstanceId
      identifiers:
        id: instance-id
        name: tag:Name


In the piece of code above (see `<virga/providers/aws.yaml>`_) we say that for the ``subnets`` section we are going to
instantiate a *client* and invoke an *action* identifying the resources we want to filter with **id** or with **name**.

The same concept is applied to the ``instances``.

This configuration file is unlikely to be changed as contains information depending on the underlying library (in this
case boto3_) but in case we want to add new sections or defining different identifiers, we can use the provided file
as template and override the default definition file with the option ``-definition``.


Tests
=====

An example is worth 1000 words.

You want to know if the subnet ``my-subnet`` on AWS has:

* the CIDR block equals to 10.0.0.0/24
* set the tag *environment* with the value *staging*

and then you want to know if the EC2 instances with the tag name starting with the value ``my-app`` are in the subnet
``my-subnet``.

According to the definition, our ``test.yaml`` will be

.. code:: yaml

    ---
    provider:
      name: aws
      params:
        region_name: eu-west-2
      extra:
        role_arn: arn:aws:iam::0123456789:role/Tests
    tests:
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

The ``provider`` section specify the parameters for connecting our client to AWS.

The ``tests`` section declares two scopes for the tests: ``subnets`` and ``instances`` and the resources are
identified with the ``subnet-id`` for the subnet and with the ``tag:Name`` for the EC2 instances.

The ``assertions`` are the actual tests: each item represents a condition to verify using the query language JMESPath_.

The only exception is the last assertion

.. code::yaml

    SubnetId=="_lookup('subnets', 'name', 'my-subnet')"

``_lookup`` is a Virga function that returns the subnet ID from:

* the context
* the identifier (eg. name or id)
* the value to search

_lookup function
================

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
