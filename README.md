# Automatically bumping Semantic Versioning in Gitlab CI
The idea was that in order to continuously deliver whilst keeping Semantic Versioning, we needed an automation step. 
This aims to do that, it's not perfect, but it's better than tagging manually or worse, forgetting to tag. It was mainly
designed to work with GitLab, it can be quite easily extended to also work with other tools.

## Pre-requisites
In order to make this work you need a user that has access to your repository and have it's SSH private key in a 
environment variable, as well as the public key added to its account.


## Example .gitlab-ci.yml
Below is an example of using it in GitLab CI. First we inject the SSH key of the user with sufficient rights to push to
a repository.

Then we call the `auto-semver` command to do its thing. This step will only be triggered on the branch `main` assuming 
that this is the branch you merge your development branch to. 

Given that `auto-semver` actually pushes to your repository it will trigger a new pipeline, steps such as `deploy` are 
then activated but not `publish`. 

Ideally you should change `latest` to a pinned version.

```yaml
auto-semver:
  stage: publish
  image: freddegier/gitlab-auto-semver:latest
  script:
    - mkdir -p ~/.ssh && echo "$SEMVER_SSH_KEY" > ~/.ssh/id_rsa && chmod -R 700 ~/.ssh
    - auto-semver
  rules:
    - if: $CI_COMMIT_REF_NAME == 'main'

deploy:
  stage: deploy
  script:
    - echo "Deploying"
  rules:
    - if: $CI_COMMIT_TAG
```
