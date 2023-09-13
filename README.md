# ChatGPT + ACSS data with Azure OpenAI and Cognitive Search

Python version 3.9.13

## Steps to create a local docker image and push to azure container registry

## Commands

 docker build -t copilotsapregistry.azurecr.io/<image-name>:<tag> .
 docker push copilotsapregistry.azurecr.io/<image-name>:<tag>

## Example

 docker build -t copilotsapregistry.azurecr.io/hstest:v1 .
 docker push copilotsapregistry.azurecr.io/hstest:v1
