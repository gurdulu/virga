# List of mapped AWS resources

Context|Description|Client|Definition file|Identifier key|Filter
---|---|---|---|---|---
| elb | Classic ELB | virga | [elb.yaml](../virga/providers/aws/definitions/elb.yaml) | name | {"key": "name", "type": "string"} |
| addresses | Elastic IPs | ec2 | [addresses.yaml](../virga/providers/aws/definitions/addresses.yaml) | id | {"key": "public-ip", "type": "filter"} |
|  |  |  |  | name | {"key": "tag:Name", "type": "filter"} |
| instances | EC2 Instances | ec2 | [instances.yaml](../virga/providers/aws/definitions/instances.yaml) | id | {"key": "instance-id", "type": "filter"} |
|  |  |  |  | name | {"key": "tag:Name", "type": "filter"} |
| cloudtrails | CloudTrails | virga | [cloudtrails.yaml](../virga/providers/aws/definitions/cloudtrails.yaml) | name | {"key": "name", "type": "string"} |
| vpc_peering_connections | VPC Peering Connections | ec2 | [vpc_peering_connections.yaml](../virga/providers/aws/definitions/vpc_peering_connections.yaml) | name | {"key": "tag:Name", "type": "filter"} |
| certificates | ACM Certificates | virga | [certificates.yaml](../virga/providers/aws/definitions/certificates.yaml) | domain_name | {"key": "domain-name", "type": "string"} |
| security_groups | Security Groups | ec2 | [security_groups.yaml](../virga/providers/aws/definitions/security_groups.yaml) | id | {"key": "group-id", "type": "filter"} |
|  |  |  |  | name | {"key": "tag:Name", "type": "filter"} |
|  |  |  |  | group_name | {"key": "group-name", "type": "filter"} |
| db_instances | RDS instances | rds | [db_instances.yaml](../virga/providers/aws/definitions/db_instances.yaml) | id | {"key": "db-instance-id", "type": "filter"} |
| vpcs | VPC | ec2 | [vpcs.yaml](../virga/providers/aws/definitions/vpcs.yaml) | name | {"key": "tag:Name", "type": "filter"} |
| cloudformation_stacks | Cloud Formation Stacks | cloudformation | [cloudformation_stacks.yaml](../virga/providers/aws/definitions/cloudformation_stacks.yaml) | name | {"key": "StackName", "type": "string"} |
| route_tables | Route tables | ec2 | [route_tables.yaml](../virga/providers/aws/definitions/route_tables.yaml) | id | {"key": "route-table-id", "type": "filter"} |
|  |  |  |  | name | {"key": "tag:Name", "type": "filter"} |
| auto_scaling_groups | Auto Scaling Groups | virga | [auto_scaling_groups.yaml](../virga/providers/aws/definitions/auto_scaling_groups.yaml) | name | {"key": "AutoScalingGroupNames", "type": "string"} |
| elbv2 | ELB v2 | virga | [elbv2.yaml](../virga/providers/aws/definitions/elbv2.yaml) | name | {"key": "name", "type": "string"} |
| network_acls | Network ACLs | ec2 | [network_acls.yaml](../virga/providers/aws/definitions/network_acls.yaml) | id | {"key": "network-acl-id", "type": "filter"} |
|  |  |  |  | name | {"key": "tag:Name", "type": "filter"} |
| subnets | Subnets | ec2 | [subnets.yaml](../virga/providers/aws/definitions/subnets.yaml) | id | {"key": "subnet-id", "type": "filter"} |
|  |  |  |  | name | {"key": "tag:Name", "type": "filter"} |
| images | AMI | ec2 | [images.yaml](../virga/providers/aws/definitions/images.yaml) | id | {"key": "image-id", "type": "filter"} |
|  |  |  |  | name | {"key": "name", "type": "filter"} |
