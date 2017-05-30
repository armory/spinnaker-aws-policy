#!/bin/bash
set -e

mkdir /spinnaker
cd /spinnaker
git clone https://github.com/spinnaker/clouddriver.git 1>&2
/src/generate.py /spinnaker/clouddriver/clouddriver-aws
