import datetime

from dateutil.tz import tzutc


acm_certificate_list = {
    'CertificateSummaryList': [
        {
            'DomainName': 'my.any-domain.com',
            'CertificateArn': 'arn:aws:acm:eu-west-2:012345678:certificate/01234567-abcd-0123-0123-abcdfe01234'
        }
    ]
}


acm_result_find_certificate = {
    'CertificateArn': 'arn:aws:acm:eu-west-2:012345678:certificate/01234567-abcd-0123-0123-abcdfe01234',
    'CreatedAt': '2017-01-11T09:23:40+01:00',
    'DomainName': 'my.any-domain.com',
    'DomainValidationOptions': [
        {
            'DomainName': 'my.any-domain.com',
            'ValidationDomain': 'any-domain.com',
            'ValidationEmails': [
                'hostmaster@any-domain.com',
                'admin@any-domain.com',
                'webmaster@any-domain.com',
                'postmaster@any-domain.com',
                'administrator@any-domain.com'
            ],
            'ValidationStatus': 'SUCCESS'
        }
    ],
    'InUseBy': [],
    'IssuedAt': '2017-01-11T09:25:15+01:00',
    'Issuer': 'Amazon',
    'KeyAlgorithm': 'RSA-2048',
    'NotAfter': '2018-01-12T13:00:00+01:00',
    'NotBefore': '2017-01-12T01:00:00+01:00',
    'Serial': '00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd:ee:ff',
    'SignatureAlgorithm': 'SHA256WITHRSA',
    'Status': 'ISSUED',
    'Subject': 'CN=my.any-domain.com',
    'SubjectAlternativeNames': ['my.any-domain.com'],
    'Type': 'AMAZON_ISSUED'
}


elbv2_describe_load_balancers = {
    'LoadBalancers': [
        {
            'AvailabilityZones': [
                {
                    'SubnetId': 'subnet-0123456',
                    'ZoneName': 'eu-west-2a'
                },
                {
                    'SubnetId': 'subnet-0123457',
                    'ZoneName': 'eu-west-2b'}
            ],
            'CanonicalHostedZoneId': 'ZHURV9DERC5T8',
            'CreatedTime': datetime.datetime(2017, 1, 12, 8, 25, 11, 840000, tzinfo=tzutc()),
            'DNSName': 'internal-my-elbv2-018826633.eu-west-2.elb.amazonaws.com',
            'IpAddressType': 'ipv4',
            'LoadBalancerArn': 'arn:aws:elasticloadbalancing:eu-west-2:01234567890:loadbalancer/app/my-elbv2/9987acf27',
            'LoadBalancerName': 'my-elbv2',
            'Scheme': 'internal',
            'SecurityGroups': ['sg-02232883'],
            'State': {'Code': 'active'},
            'Type': 'application',
            'VpcId': 'vpc-9839873'}
    ]
}


elbv2_describe_load_balancer_attributes = {
    'Attributes': [
        {'Key': 'access_logs.s3.bucket', 'Value': 'bucket'},
        {'Key': 'deletion_protection.enabled', 'Value': 'false'},
        {'Key': 'access_logs.s3.prefix', 'Value': 'prefix'},
        {'Key': 'idle_timeout.timeout_seconds', 'Value': '60'},
        {'Key': 'access_logs.s3.enabled', 'Value': 'false'}
    ],
}


elbv2_describe_listeners = {
    'Listeners': [
        {
            'DefaultActions': [
                {
                    'TargetGroupArn': 'arn:aws:elasticloadbalancing:eu-west-2:12345679012:targetgroup/my-app-tg/0bd28872872',
                    'Type': 'forward'
                }
            ],
            'ListenerArn': 'arn:aws:elasticloadbalancing:eu-west-2:01234567890:listener/app/my-elbv2/9b54/2ab1',
            'LoadBalancerArn': 'arn:aws:elasticloadbalancing:eu-west-2:01234567890:loadbalancer/app/my-elbv2/9987acf27',
            'Port': 8080,
            'Protocol': 'HTTP'
        }
    ]
}


elbv2_describe_target_groups = {
    'TargetGroups': [
        {
            'HealthCheckIntervalSeconds': 30,
            'HealthCheckPath': '/',
            'HealthCheckPort': 'traffic-port',
            'HealthCheckProtocol': 'HTTP',
            'HealthCheckTimeoutSeconds': 5,
            'HealthyThresholdCount': 5,
            'LoadBalancerArns': [
                'arn:aws:elasticloadbalancing:eu-west-2:01234567890:loadbalancer/app/my-elbv2/9987acf27'
            ],
            'Matcher': {'HttpCode': '200'},
            'Port': 8080,
            'Protocol': 'HTTP',
            'TargetGroupArn': 'arn:aws:elasticloadbalancing:eu-west-2:12345679012:targetgroup/my-app-tg/0bd28872872',
            'TargetGroupName': 'my-app-tg',
            'TargetType': 'instance',
            'UnhealthyThresholdCount': 2,
            'VpcId': 'vpc-9839873'
        }
    ]
}


elbv2_describe_target_group_attributes = {
    'Attributes': [
        {'Key': 'stickiness.enabled', 'Value': 'true'},
        {'Key': 'deregistration_delay.timeout_seconds', 'Value': '300'},
        {'Key': 'stickiness.type', 'Value': 'lb_cookie'},
        {'Key': 'stickiness.lb_cookie.duration_seconds', 'Value': '86400'}
    ],
}


elbv2_result = {
    'LoadBalancers': [
        {
            'Attributes': [
                {'Key': 'access_logs.s3.bucket', 'Value': 'bucket'},
                {'Key': 'deletion_protection.enabled', 'Value': 'false'},
                {'Key': 'access_logs.s3.prefix', 'Value': 'prefix'},
                {'Key': 'idle_timeout.timeout_seconds', 'Value': '60'},
                {'Key': 'access_logs.s3.enabled', 'Value': 'false'}
            ],
            'AvailabilityZones': [
                {'SubnetId': 'subnet-0123456', 'ZoneName': 'eu-west-2a'},
                {'SubnetId': 'subnet-0123457', 'ZoneName': 'eu-west-2b'}
            ],
            'CanonicalHostedZoneId': 'ZHURV9DERC5T8',
            'CreatedTime': datetime.datetime(2017, 1, 12, 8, 25, 11, 840000, tzinfo=tzutc()),
            'DNSName': 'internal-my-elbv2-018826633.eu-west-2.elb.amazonaws.com',
            'IpAddressType': 'ipv4',
            'Listeners': [
                {
                    'DefaultActions': [
                        {
                            'TargetGroupArn': 'arn:aws:elasticloadbalancing:eu-west-2:12345679012:targetgroup/my-app-tg/0bd28872872',
                            'Type': 'forward'
                        }
                    ],
                    'ListenerArn': 'arn:aws:elasticloadbalancing:eu-west-2:01234567890:listener/app/my-elbv2/9b54/2ab1',
                    'LoadBalancerArn': 'arn:aws:elasticloadbalancing:eu-west-2:01234567890:loadbalancer/app/my-elbv2/9987acf27',
                    'Port': 8080,
                    'Protocol': 'HTTP'
                }
            ],
            'LoadBalancerArn': 'arn:aws:elasticloadbalancing:eu-west-2:01234567890:loadbalancer/app/my-elbv2/9987acf27',
            'LoadBalancerName': 'my-elbv2',
            'Scheme': 'internal',
            'SecurityGroups': ['sg-02232883'],
            'State': {'Code': 'active'},
            'TargetGroups': [
                {
                    'Attributes': [
                        {'Key': 'stickiness.enabled', 'Value': 'true'},
                        {'Key': 'deregistration_delay.timeout_seconds', 'Value': '300'},
                        {'Key': 'stickiness.type', 'Value': 'lb_cookie'},
                        {'Key': 'stickiness.lb_cookie.duration_seconds', 'Value': '86400'}
                    ],
                    'HealthCheckIntervalSeconds': 30,
                    'HealthCheckPath': '/',
                    'HealthCheckPort': 'traffic-port',
                    'HealthCheckProtocol': 'HTTP',
                    'HealthCheckTimeoutSeconds': 5,
                    'HealthyThresholdCount': 5,
                    'LoadBalancerArns': [
                        'arn:aws:elasticloadbalancing:eu-west-2:01234567890:loadbalancer/app/my-elbv2/9987acf27'
                    ],
                    'Matcher': {'HttpCode': '200'},
                    'Port': 8080,
                    'Protocol': 'HTTP',
                    'TargetGroupArn': 'arn:aws:elasticloadbalancing:eu-west-2:12345679012:targetgroup/my-app-tg/0bd28872872',
                    'TargetGroupName': 'my-app-tg',
                    'TargetType': 'instance',
                    'UnhealthyThresholdCount': 2,
                    'VpcId': 'vpc-9839873'
                }
            ],
            'Type': 'application',
            'VpcId': 'vpc-9839873'
        }
    ]
}
