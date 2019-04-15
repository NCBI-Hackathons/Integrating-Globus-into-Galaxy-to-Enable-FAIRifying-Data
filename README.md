# Integrating-Globus-into-Galaxy-to-Enable-FAIRifying-Data

## Goals

Things we'd like to get out of this hackathon

* A how to on setting up Galaxy using Globus Auth. There are examples of doing this for [Atlassian products](https://globus-integration-examples.readthedocs.io/en/latest/atlassian.html) and [WordPress](https://globus-integration-examples.readthedocs.io/en/latest/wordpress.html) for reference. This currently requires the Galaxy dev branch because of the version dependency on [Python Social Auth](https://python-social-auth-docs.readthedocs.io/). Enabling Globus Auth requires  changes in `config/galaxy.yml` to enable OIDC and the necessary specify `client_id`, `client_secret`, and a callback URI (which is a redirect URI) in `config/oidc_backend_config.xml`.

* A Galaxy Tool template that can get securely get tokens from a user’s Galaxy environment (I.e., without using a stored database password)

* A Galaxy tool for Transfer with inputs and outputs for endpoints and paths. We want this tool to end up in the Galaxy toolshed.

* Either another tool or the same one to create folders and set permissions on a shared endpoint, similar to things we do in the [Globus automation examples](https://github.com/globus/automation-examples/)

* Sample workflows to use these.

## FAIRness

[FAIRshake](https://fairshake.cloud) has different rubrics, the [tool rubric](https://fairshake.cloud/rubric/7/) seems the most appropriate.


# 2 Teams

## 1 - A Galaxy user can use a remote endpoint (Globus managed) to transfer data into the instance for a workflow

1. create a galaxy workflow
2. create a step to import data
3. create **galaxy tool** to use globus endpoints
4. install tool on our galaxy instance
5. configure step workflow to use our tool
 a. create a globus managed link (dep)
6. validate the data was transferred from a Globus into Galaxy
