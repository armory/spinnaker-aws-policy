#!/usr/bin/env python3

import unittest
import generate
import json
import os


class TestGeneratePolicy(unittest.TestCase):

    def test_all(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        json_policy = json.loads(generate.policy(
            dir_path + "/clouddriver-aws/"))
        expected = {
            "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
            "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
            "elasticloadbalancing:RegisterTargets",
            "elasticloadbalancing:DeregisterTargets",
            "ec2:DescribeRegions",
            "ec2:DescribeAvailabilityZones",
            "ec2:DescribeSecurityGroups",
            "ec2:DescribeVpcs",
            "iam:PassRole"
        }
        self.assertEquals(expected, set(json_policy['Statement'][0]['Action']))
