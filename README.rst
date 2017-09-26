=====
Virga
=====

From `Wikipedia <https://en.wikipedia.org/wiki/Virga>`_: *"In meteorology, Virga is an observable streak or shaft of
precipitation falling from a cloud that evaporates or sublimates before reaching the ground."*

This piece of software is not about a weather phenomenon. In this context Virga is a tool for analysing your Cloud
infrastructure before the rain reaches the ground.

----------------------------------
This project is still in pre-alpha
----------------------------------

There are many things still missing:

* the documentation needs to be written better
* the definition file is just a draft for testing purposes
* it needs tests on real data resources

------------------
Provider supported
------------------

At the moment only `AWS <https://aws.amazon.com/>`_.

------------
Requirements
------------

* `Python 3.5+ <https://www.python.org/>`_
* `PyYAML <http://pyyaml.org/wiki/PyYAML>`_
* `JMESPath.py <https://github.com/jmespath/jmespath.py>`_

Specific for AWS
================

* an AWS working account
* `boto3 <https://github.com/boto/boto3>`_

-----------
Quick start
-----------

1. Install Virga :code:`pip install virga`
2. Edit the file ``template.yaml``
3. :code:`virga template.yaml`


``template.yaml`` is the `Configuration file`_.

------------------
Configuration file
------------------

See `This project is still in pre-alpha`_

An example is worth 1000 words.

You want to know if the subnet ``my-subnet`` on AWS has:

* the CIDR block equals to 10.0.0.0/24
* set the tag *environment* with the value *staging*

and then you want to know if the EC2 instances with the tag name starting with the value ``my-app`` are in the subnet
``my-subnet``.

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
        - name: my-subnet
          assertions:
            - CidrBlock==`10.0.0.0/24`
            - Tags[?Key==`environment` && Value == `staging`]
      instances:
        - name: my-app-*
          assertions:
            - SubnetId=="_lookup('subnets', 'name', 'my-subnet')"

The first section ``provider`` sets the provider you want to use and the way you want to use it:

* **name** must be an existing module in the ``providers`` module
* **params** contains settings for the client connection
* **extra** can be used for additional actions required by the provider

The second section ``tests`` define the battery of tests.

For understanding this section we need to refer to the definition file.

For example the ``subnets`` section is defined

.. code::yaml

    subnets:
      client: ec2
      action: describe_subnets
      context: Subnets
      prefix: Subnets
      resource_id: SubnetId
      identifiers:
        id: subnet-id
        name: tag:Name

The tag ``name`` is defined as ``tag:Name`` and is used for filtering the resources tagged **Name**.

Then declare a **section** ``tests`` with two **context** ``subnets`` and ``instances``. For each context declare
the list of resources to evaluate and the list of assertions for each resource.

Because you don't know the subnet ID, you can use the interpolated `_lookup function`_ that accepts three parameters:

* the context
* the identifier (eg. name or id)
* the value to search

The assertions are declarations made with the query language `JMESPath <http://jmespath.org/>`_.

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

* `List of AWS resources <docs/resource_mapping_aws.html>`_

---------------
Advanced topics
---------------

* `Definition file <docs/definition_file.rst>`_
* `How to build a custom provider <docs/custom_provider.rst>`_
