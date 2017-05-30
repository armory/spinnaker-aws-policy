# spinnaker-aws-policy


## Clouddriver

To generate an AWS Policy for the current head of Spinnaker Clouddriver:

    ./bin/build
    ./bin/run

The policy will be printed to stdout. It will contain all of the necessary actions for Spinnaker's Clouddriver to operate. If you wish, you can isolate any of the actions to certain resources by modifying the policy after it is generated.

### Running Locally

If you have a checkout of Clouddriver locally and want to generate the policy for it you can run the python script directly on your development system:

    Run `src/generate.py <CLOUDDRIVER_AWS_DIRECTORY>`

where `<CLOUDDRIVER_AWS_DIRECTORY>` is the location on disk of the clouddriver github repo checked out to which ever version you want to generate the policy for.

The policy will be printed to stdout. It will contain all of the necessary actions for Spinnaker's Clouddriver to operate. If you wish, you can isolate any of the actions to certain resources by modifying the policy after it is generated.


### How does it work?

The generator searches the clouddriver codebase for calls to the AWS API. It maps any API calls to their required permissions.

_Note:_ The method for generating the policy is imperfect, but considered 'good enough'.

## Rosco

The policy that Spinnaker's Rosco requires is a bit different. Since Rosco uses Packer, you can consult HashiCorp's recommendation [here](https://www.packer.io/docs/builders/amazon.html).
