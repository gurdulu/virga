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
            'SecurityGroups': ['sg-01992883'],
            'State': {'Code': 'active'},
            'Type': 'application',
            'VpcId': 'vpc-9839873'}
    ]
}
