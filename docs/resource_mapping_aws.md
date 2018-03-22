
# List of mapped AWS resources

| Context | Description | Client | Identifier key | Identifier value |
|---|---|---|---|---|
| addresses | EIP | ec2 | ip | {'key': 'public-ip', 'type': 'filter'} |
|   |   |   | name | {'key': 'tag:Name', 'type': 'filter'} |
| amis | AMI | ec2 | id | {'key': 'image-id', 'type': 'filter'} |
|   |   |   | name | {'key': 'name', 'type': 'filter'} |
| autoscaling_groups | Auto Scaling Group | virga | name | {'key': 'AutoScalingGroupNames', 'type': 'string'} |
| certificates | ACM Certificates | virga | domain_name | {'key': 'domain-name', 'type': 'string'} |
| stacks | Cloud Formation Stacks | cloudformation | name | {'key': 'StackName', 'type': 'string'} |
| cloudtrails | CloudTrails | virga | name | {'key': 'name', 'type': 'string'} |
| db_instances | RDS instances | rds | id | {'key': 'db-instance-id', 'type': 'filter'} |
| elbv2 | ELB v2 | virga | name | {'key': 'name', 'type': 'string'} |
| instances | EC2 Instances | ec2 | id | {'key': 'instance-id', 'type': 'filter'} |
|   |   |   | name | {'key': 'tag:Name', 'type': 'filter'} |
| network_acls | Network ACLs | ec2 | id | {'key': 'network-acl-id', 'type': 'filter'} |
|   |   |   | name | {'key': 'tag:Name', 'type': 'filter'} |
| route_tables | Route tables | ec2 | id | {'key': 'route-table-id', 'type': 'filter'} |
|   |   |   | name | {'key': 'tag:Name', 'type': 'filter'} |
| security_groups | Security Groups | ec2 | id | {'key': 'group-id', 'type': 'filter'} |
|   |   |   | name | {'key': 'tag:Name', 'type': 'filter'} |
|   |   |   | group_name | {'key': 'group-name', 'type': 'filter'} |
| subnets | Subnets | ec2 | id | {'key': 'subnet-id', 'type': 'filter'} |
|   |   |   | name | {'key': 'tag:Name', 'type': 'filter'} |
| vpc_peerings | VPC Peering Connections | ec2 | name | {'key': 'tag:Name', 'type': 'filter'} |
| vpcs | VPC | ec2 | name | {'key': 'tag:Name', 'type': 'filter'} |

