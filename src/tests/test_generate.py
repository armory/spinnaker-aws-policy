#!/usr/bin/env python3

import unittest
import generate
import json


class TestGeneratePolicy(unittest.TestCase):

    def test_all(self):
        json_policy = json.loads(generate.policy(
            "/Users/Andrew/armory/spinnaker-aws-policy/src/tests/clouddriver-aws/"))
        expected = {
            "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
            "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
            "elasticloadbalancingv2:RegisterTargets",
            "elasticloadbalancingv2:DeregisterTargets",
            "ec2:DescribeRegions",
            "ec2:DescribeAvailabilityZones",
            "ec2:DescribeSecurityGroups",
            "ec2:DescribeVpcs",
            "iam:PassRole"
        }
        self.assertEquals(expected, set(json_policy['Statement'][0]['Action']))
