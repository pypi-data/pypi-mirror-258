# coding: utf-8

"""
    Nuon

    API for managing nuon apps, components, and installs.

    The version of the OpenAPI document: 0.19.15
    Contact: support@nuon.co
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from nuon.models.service_create_install_request_aws_account import ServiceCreateInstallRequestAwsAccount

class TestServiceCreateInstallRequestAwsAccount(unittest.TestCase):
    """ServiceCreateInstallRequestAwsAccount unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ServiceCreateInstallRequestAwsAccount:
        """Test ServiceCreateInstallRequestAwsAccount
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ServiceCreateInstallRequestAwsAccount`
        """
        model = ServiceCreateInstallRequestAwsAccount()
        if include_optional:
            return ServiceCreateInstallRequestAwsAccount(
                iam_role_arn = '',
                region = 'us-east-1'
            )
        else:
            return ServiceCreateInstallRequestAwsAccount(
                iam_role_arn = '',
        )
        """

    def testServiceCreateInstallRequestAwsAccount(self):
        """Test ServiceCreateInstallRequestAwsAccount"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
