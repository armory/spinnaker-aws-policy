
import unittest
import generate
import policy_diff
import json
import os
import logging

logger = logging.getLogger(__name__)


MOCK_GENERATED_POLICY = """
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1486065689000",
            "Effect": "Allow",
            "Action": [
                "autoscaling:CreateAutoScalingGroup",
                "autoscaling:CreateLaunchConfiguration",
                "autoscaling:CreateOrUpdateTags",
                "autoscaling:DeleteAutoScalingGroup",
                "autoscaling:DeleteLaunchConfiguration",
                "autoscaling:DeletePolicy",
                "autoscaling:DeleteScheduledAction",
                "autoscaling:DeleteTags",
                "autoscaling:DescribeAutoScalingGroups",
                "elasticloadbalancing:ModifyLoadBalancerAttributes",
                "elasticloadbalancing:ModifyTargetGroup",
                "elasticloadbalancing:ModifyTargetGroupAttributes",
                "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
                "elasticloadbalancing:RegisterTargets",
                "elasticloadbalancing:SetLoadBalancerPoliciesOfListener",
                "elasticloadbalancing:SetSecurityGroups",
                "iam:PassRole"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}


"""
# note the extra spaces, part of the test is to make sure those are strip()'ed'
class TestPolicyDiff(unittest.TestCase):

    def test_diff(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        #json_policy = json.loads(generate.policy(dir_path + "/clouddriver-aws/")
        differ, latest_policy = policy_diff.eval_generated_from_latest_policy(MOCK_GENERATED_POLICY, "%s/policies" % dir_path)
        logger.info(differ)
        logger.info("%s \nlatest policy" % latest_policy)
        logger.info("%s \ngenerated policy" % MOCK_GENERATED_POLICY)
        self.assertTrue(differ)

    def test_diff_fail(self):
        #expects policy generator to eval to a different policy
        dir_path = os.path.dirname(os.path.realpath(__file__))
        #json_policy = json.loads(generate.policy(dir_path + "/clouddriver-aws/")
        mock_policy = MOCK_GENERATED_POLICY + "\nMAKE_TEST_FAIL"
        differ, latest_policy = policy_diff.eval_generated_from_latest_policy(mock_policy, "%s/policies" % dir_path)
        logger.info(differ)
        logger.info("%s \nlatest policy" % latest_policy)
        logger.info("%s \ngenerated policy" % mock_policy)
        self.assertFalse(differ)
