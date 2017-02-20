#!/usr/bin/env python3

import ec2
import elb
import elbv2
import autoscaling
import cloudwatch
import os
import sys
import iam
from collections import defaultdict

policy_template = """
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1486065689000",
            "Effect": "Allow",
            "Action": [
%s                "iam:PassRole"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
"""


def _format(s):
    formatted = set()
    for x in s:
        formatted.add(x.title().replace("-", ""))
    return formatted


# TODO(andrewbackes): Figure out a way to pull the API calls from boto3.
_action_map = {
    "ec2": _format(ec2.actions),
    "elasticloadbalancing": _format(elb.actions),
    "elasticloadbalancingv2": _format(elbv2.actions),
    "autoscaling": _format(autoscaling.actions),
    "iam": _format(iam.actions),
    "cloudwatch": _format(cloudwatch.actions)
}


def _parse_actions(filename):
    """Run through the file looking for imported AWS libraries. Then look
    for calls from that library.
    """
    requested_action = set()
    imports = defaultdict(set)

    def imported(k, v):
        if imports.get(k) and "*" in imports[k]:
            return True
        else:
            for i in imports.get(k, {}):
                if v in i:
                    return True
        return False

    def import_handler(resource):
        import_path = resource.split('.')
        if len(import_path) >= 6:
            collection = import_path[3]
            resource = import_path[5]
            if resource.endswith(";"):
                resource = resource[:-1]
            if import_path[1] == "amazonaws" and collection in _action_map.keys():
                imports[collection].add(resource.lower())

    def action_handler(resource):
        actions = set()
        for k, v in _action_map.items():
            for a in v:
                if a.lower() in resource.lower() and imported(k, a.lower()):
                    actions.add(k + ":" + a)
        requested_action.update(actions)

    def handle(line):
        if line.startswith("import"):
            import_handler(line.split()[1])
        else:
            for word in line.split():
                action_handler(word)

    with open(filename, 'r') as f:
        for line in f:
            handle(line)
    return requested_action


def _get_actions(clouddriver_aws_dir):
    """Walk the clouddriver-aws directory looking for java/groovy files that use
    the AWS SDK. From there analyse which AWS API calls are made.
    """
    actions = set()

    def could_contain_actions(abs_path):
        groovy = abs_path.endswith(".groovy")
        java = abs_path.endswith(".java")
        return java or groovy

    for root, dirs, files in os.walk(clouddriver_aws_dir):
        for file in files:
            abs_path = root + os.sep + file
            if could_contain_actions(abs_path):
                actions.update(_parse_actions(abs_path))
    return actions


def policy(clouddriver_aws_dir):
    """Generate a valid AWS IAM Policy with close to minimal permissions needed
    by the codebase.
    """
    actions = _get_actions(clouddriver_aws_dir)
    new_map = {}
    for k, v in _action_map.items():
        new_map[k] = set()
        for action in actions:
            if action.startswith(k):
                new_map[k].add(action)
        if len(new_map[k]) == len(v):
            new_map[k] = {k + ":*"}
    stringified_actions = ""
    for v in set(new_map.values()):
        for action in v:
            stringified_actions = stringified_actions + \
                '                "' + action + '",\n'
    policy = policy_template % (stringified_actions)
    return policy


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        clouddriver_dir = sys.argv[1]
    elif os.environ.get('CLOUDDRIVER_AWS_DIR', None):
        clouddriver_dir = os.environ['CLOUDDRIVER_AWS_DIR']
    else:
        print("Usage:\n\t policy.py <CLOUDDRIVER_AWS_DIR>\n")
        sys.exit(1)
    print(policy(clouddriver_dir))
