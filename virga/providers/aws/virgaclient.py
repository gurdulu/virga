import boto3
import re
from botocore.exceptions import ClientError

from virga.common import VirgaException


class VirgaClient(object):
    """VirgaClient substitute the standard AWS client for more complex requests."""

    @staticmethod
    def find_certificate(resource_object: dict) -> any:
        """
        Call boto3/acm for finding the certificate for the passed domain.

        :param resource_object: Object filter
        :return: Response from AWS
        """
        client = boto3.client('acm')
        certificates = client.list_certificates()
        try:
            res_certificates = [
                cert for cert in certificates['CertificateSummaryList']
                if cert['DomainName'] == resource_object['domain_name']
            ]
            return client.describe_certificate(CertificateArn=res_certificates[0]['CertificateArn'])
        except ClientError:
            raise VirgaException('Lookup certificates domain_name %s failed' % resource_object['domain_name'])
        except (KeyError, IndexError):
            return None

    @staticmethod
    def find_elbv2(resource_object: dict) -> any:
        """
        Call boto3/elbv2 for finding the ELBv2 instance by name.

        The result contains:
        - load balancer attributes
        - listeners
        - target groups
        - target group attributes

        :param resource_object: Object filter
        :return: Response from AWS
        """
        client = boto3.client('elbv2')
        try:
            resources = client.describe_load_balancers()
            resource = [
                x for x in resources['LoadBalancers'] if x['LoadBalancerName'] == resource_object['name']
            ][0]

            arn = resource['LoadBalancerArn']
            attributes = client.describe_load_balancer_attributes(LoadBalancerArn=arn)

            resource['Attributes'] = attributes['Attributes']
            listeners = client.describe_listeners(LoadBalancerArn=arn)

            resource['Listeners'] = listeners['Listeners']
            target_groups = client.describe_target_groups(LoadBalancerArn=arn)

            result_target_group = []
            for target_group in target_groups['TargetGroups']:
                attributes = client.describe_target_group_attributes(
                    TargetGroupArn=target_group['TargetGroupArn'])['Attributes']
                target_group['Attributes'] = attributes
                result_target_group.append(target_group)

            resource['TargetGroups'] = result_target_group

            return {'LoadBalancers': [resource]}
        except ClientError:
            raise VirgaException('Lookup %s %s %s failed' % ('elbv2', 'name', resource_object['name']))
        except (KeyError, IndexError):
            return None

    @staticmethod
    def find_cloudtrail(resource_object: dict) -> dict:
        """
        Call boto3/cloudtrail for finding the CloudTrail trail by name.

        :param resource_object: Object filter
        :return: Response from AWS
        """
        client = boto3.client('cloudtrail')
        response = client.describe_trails()
        return {'trailList': list(filter(lambda d: d['Name'] == resource_object['name'], response['trailList']))}

    @staticmethod
    def find_auto_scaling_groups(resource_object: dict) -> dict:
        """
        Call boto3/autoscaling for finding the AutoScaling group by name.

        :param resource_object: Object filter
        :return: Response from AWS
        """
        client = boto3.client('autoscaling')
        response = client.describe_auto_scaling_groups()
        group_names = [x['AutoScalingGroupName'] for x in response['AutoScalingGroups']]
        regex = re.compile(resource_object['name'].replace('*', '.*'))
        group_names = filter(regex.search, group_names)
        groups = [x for x in response['AutoScalingGroups'] if x['AutoScalingGroupName'] in group_names]
        return {'AutoScalingGroups': groups}
