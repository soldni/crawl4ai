#! /usr/bin/env bash

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

docker tag oe-base/crawl4ai:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/oe-base/crawl4ai:latest
