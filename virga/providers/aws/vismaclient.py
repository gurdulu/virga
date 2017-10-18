import boto3

from virga.exceptions import VirgaException


class VismaClient(object):

    def __init__(self, params):
        self.params = params

    def find_certificate(self, resource_definition: dict, resource_object: dict) -> dict:
        """
        Call boto3/acm for finding the certificate for the passed domain.

        :param resource_definition: Section definition
        :param resource_object: Object filter
        :return: Response from AWS
        """
        client = boto3.client('acm', **self.params)
        certificates = client.list_certificates()
        try:
            res_certificates = [
                cert for cert in certificates['CertificateSummaryList']
                if cert['DomainName'] == resource_object['domain_name']
            ]
            return client.describe_certificate(CertificateArn=res_certificates[0]['CertificateArn'])
        except (KeyError, IndexError):
            raise VirgaException(
                'Lookup %s %s %s failed' % ('certificates', 'domain_name', resource_object['domain_name']))
