#!/bin/bash
mkdir /spinnaker
cd /spinnaker
git clone -b release-1.8.x https://github.com/spinnaker/clouddriver.git 1>&2
echo "executing policy-diff"
/src/policy_diff.py /spinnaker/clouddriver/clouddriver-aws
