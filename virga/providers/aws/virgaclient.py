import boto3

from virga.common import VirgaException


class VirgaClient(object):
    """VirgaClient substitute the standard AWS client for more complex requests."""

    @staticmethod
    def find_certificate(resource_definition: dict, resource_object: dict) -> dict:  # NOQA
        """
        Call boto3/acm for finding the certificate for the passed domain.

        :param resource_definition: Section definition
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
        except (KeyError, IndexError):
            raise VirgaException(
                'Lookup %s %s %s failed' % ('certificates', 'domain_name', resource_object['domain_name']))
