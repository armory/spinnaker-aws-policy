#!/usr/bin/env python3

import ec2
import elb
import elbv2
import autoscaling
import cloudwatch
import os
import sys
import iam


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


def format(s):
    formatted = set()
    for x in s:
        formatted.add(x.title().replace("-", ""))
    return formatted


action_map = {
    "ec2" : format(ec2.actions),
    "elasticloadbalancing" : format(elb.actions),
    "elasticloadbalancingv2": format(elbv2.actions),
    "autoscaling": format(autoscaling.actions),
    "iam": format(iam.actions),
    "cloudwatch": format(cloudwatch.actions)
}


def actions_of(request):
    actions = set()
    for k,v in action_map.items():
        for a in v:
            if a.lower() in request.lower():
                actions.add(k + ":" + a)
    return actions


def requests_in(filename):
    requested_action = set()
    with open(filename,'r') as f:
        for line in f:
            for word in line.split():
                requested_action = requested_action.union(actions_of(word))
    return requested_action


def aws_actions(clouddriver_aws_dir):
    actions = set()
    def could_contain_requests(abs_path):
        groovy = abs_path.endswith(".groovy")
        java = abs_path.endswith(".java")
        return java or groovy
    for root, dirs, files in os.walk(clouddriver_aws_dir):
        for file in files:
            abs_path = root + os.sep + file 
            if could_contain_requests(abs_path):
                actions = actions.union(requests_in(abs_path))
    return actions


def generate_policy(actions):
    print(actions)
    new_map = {}
    for k, v in action_map.items():
        new_map[k] = set()
        for action in actions:
            if action.startswith(k):
                new_map[k].add(action)
        if len(new_map[k]) == len(v):
            new_map[k] = { k + ":*" }
    stringified_actions = ""
    for v in new_map.values():
        for action in v:
            stringified_actions = stringified_actions + '                "' + action + '",\n'
    policy = policy_template % (stringified_actions)
    return policy


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        clouddriver_dir = sys.argv[1]
    elif os.environ.get('CLOUDDRIVER_AWS_DIR', None):  
        clouddriver_dir = os.environ['CLOUDDRIVER_AWS_DIR']
    else:
        print("Usage:\n\t generate_policy.py <CLOUDDRIVER_AWS_DIR>")
        os.exit(1)
    print(generate_policy(aws_actions(clouddriver_dir)))
