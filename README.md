# Deploy a pipeline to deliver DCV logs from an Appstream fleet to an Opensearch domain:

![Overall Architecture of APPSTREAM SESSION LATENCY](<./Appstream - Session Latency.svg>)
## Overview

This repository is part of the solution described in the blog post [here](<>) to create a solution to monitor and visualize the latency of users sessions created to Appstream servers. The repository has the required files to create the required resources to build a delivery pipeline for the DCV logs emitted from an Appstream instance to an Opensearch domain.

This repository contains an AWS SAM template that will automate the creation of the delivery pipeline resources, which consists mainly of two main components:

A. [A Kinesis Data Stream](<https://docs.aws.amazon.com/streams/latest/dev/introduction.html>)  Which will ingest the logs emitted from all configured Appstream instances, and sends them to a Lambda function.

B. A Lambda Function: Which will sends the logs it has received to the Opensearch domain.

Additionally, the AWS SAM Template will create:

C- The IAM role for Appstream Fleet: This role will allow instances in the Appstream fleet to sends the DCV logss towards the Kinesis Data stream created.


## Repo structure.

- `template.yaml` - A serverless template that defines the configuration of the resources to be deployed.

- `Lambda_code/`: A directory that contains the code for the Lambda function that selects RTT metrics from all pushed metrics.

- `events/` - Contains an event that is similar to the events the lambda function will receive from kinsis firehose. This can be used to test invoke the lambda function.

- `Opensearch/` - Has an export file of the Opensearch configurations required to index and visualize the records sent to Openseach. Specifically, it has the configuration of an index pattern, graphs, and a dashboard to do such. This file can be imported to the Opensearch created to configure it, as described in [the main blog](<>)

## Deployment Steps:

### 1. Prerequistes:

#### 1.b. Resources Prerequistes:

Before the deployment of the resources in this template, create an Opensearch domain that the Lambda function will send the metrics to.

#### 2.a. SAM Prerequistes:
The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)
* `git` CLI - [Download and Install git CLI](https://git-scm.com/downloads)


### 2. Build DCV logs delivery pipeline:

#### 2.a) Download the files of this repository, by cloning the repo using Git CLI:

```bash
git clone <repo_link>
cd appstream-session-latency-dashboard-blog/
```

#### 2.b) Deploy the SAM template:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region where the resources will be deployed to.

* **OpensearchDomainEndpoint**: The endpoint of the Opensearch domain, eg:  `search-dcv-metrics-xxxxxxxxxxxxxxxxxxxxxxxxxx.us-east-1.es.amazonaws.com`.

* **OpenSearchIndex**: The index of the metrics pushed to Opensearch. It has to meet follow the restrictions [here](<https://docs.aws.amazon.com/opensearch-service/latest/developerguide/indexing.html#indexing-naming>).

* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.

* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.


## Cleanup

To delete the application  created:

```bash
sam delete
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)