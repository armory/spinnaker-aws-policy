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


_action_map = {
    "ec2": _format(ec2.actions),
    "elasticloadbalancing": _format(elb.actions),
    "elasticloadbalancingv2": _format(elbv2.actions),
    "autoscaling": _format(autoscaling.actions),
    "iam": _format(iam.actions),
    "cloudwatch": _format(cloudwatch.actions)
}


def _parse_actions(filename):
    requested_action = set()
    imports = defaultdict(set)

    def import_handler(resource):
        import_path = resource.split('.')
        if len(import_path) >= 6:
            collection = import_path[3]
            resource = import_path[5]
            if resource.endswith(";"):
                resource = resource[:-1]
            if import_path[1] == "amazonaws" and collection in _action_map.keys():
                imports[collection].add(resource)

    def action_handler(resource):
        actions = set()
        for k, v in _action_map.items():
            for a in v:
                if a.lower() in resource.lower():
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
    print(imports)
    return requested_action


def _get_actions(clouddriver_aws_dir):
    actions = set()

    def could_contain_requests(abs_path):
        groovy = abs_path.endswith(".groovy")
        java = abs_path.endswith(".java")
        return java or groovy

    for root, dirs, files in os.walk(clouddriver_aws_dir):
        for file in files:
            abs_path = root + os.sep + file
            if could_contain_requests(abs_path):
                actions.update(_parse_actions(abs_path))
    return actions


def policy(clouddriver_aws_dir):
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
    for v in new_map.values():
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
