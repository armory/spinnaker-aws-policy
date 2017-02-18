# spinnaker-aws-policy


## Clouddriver

To generate an AWS Policy for Spinnaker Clouddriver:

    Run `src/generate.py <CLOUDDRIVER_AWS_DIRECTORY>`

where `<CLOUDDRIVER_AWS_DIRECTORY>` is the location on disk of the clouddriver github repo checked out to which ever version you want to generate the policy for.

The policy will be printed to stdout. It will contain all of the necessary actions for Spinnaker's Clouddriver to operate. If you wish, you can isolate any of the actions to certain resources by modifying the policy after it is generated.


### How does it work?

The generator searches the clouddriver codebase for calls to the AWS API. It maps any API calls to their required permissions.

## Rosco

The policy that Spinnaker's Rosco requires is a bit different. Since Rosco uses Packer, you can consult HashiCorp's recommendation [here](https://www.packer.io/docs/builders/amazon.html).
