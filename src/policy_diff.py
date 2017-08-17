#!/usr/bin/env python3
import sys
import os
from os import listdir
from os.path import isfile, join
import semantic_version
import generate
import re
import logging

logger = logging.getLogger(__name__)

def _get_semantic_version(policy_filename):
    logger.debug("getting semantic version from filename is %s:" % policy_filename)
    version = re.search("[0-9]+.[0-9]+.[0-9]+", policy_filename).group(0)
    return semantic_version.Version(version)

def _find_latest_policy(policies):
    latest_version = policies[0]
    for policy in policies[1:]:
        if _get_semantic_version(policy) > _get_semantic_version(latest_version):
            latest_version = policy
    return latest_version

def eval_generated_from_latest_policy(generated_policy, policy_dir):
    generated_policy = generated_policy.strip()
    policy_filenames = [f for f in listdir(policy_dir) if isfile(join(policy_dir, f))]
    latest_policy_filename = _find_latest_policy(policy_filenames)
    latest_policy = open("%s/%s" % (policy_dir, latest_policy_filename)).read().strip()
    if generated_policy == latest_policy:
        return (True, latest_policy)
    else:
        return (False, latest_policy)

def generate_and_evaluate(clouddriver_dir, policy_dir):
    generated_policy = generate.policy(clouddriver_dir)
    return eval_generated_from_latest_policy(generated_policy, policy_dir) + (generated_policy,)

if __name__ == '__main__':
    clouddriver_dir = None
    if len(sys.argv) >= 2:
        clouddriver_dir = sys.argv[1]
    elif os.environ.get('CLOUDDRIVER_AWS_DIR', None):
        clouddriver_dir = os.environ['CLOUDDRIVER_AWS_DIR']
    else:
        print("Usage:\n\t policy_diff.py <CLOUDDRIVER_AWS_DIR>\n")
        sys.exit(1)

    same_policy, latest, generated = generate_and_evaluate(clouddriver_dir, "/policies")
    if same_policy:
        print("generated policy and latest policy are the same")
        sys.exit(0)
    else:
        print("generated and latest policy differ!!")
        print("generated policy: \n %s" % generated)
        print("latest policy: \n %s" % latest)
        sys.exit(1)
