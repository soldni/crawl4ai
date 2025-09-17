#! /usr/bin/env bash

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1

docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/oe-base/crawl4ai:latest
