#! /usr/bin/env bash

current_dir=$(dirname $(realpath $0))

cd $current_dir/../..

bash scripts/ecr/2-build.sh

cd -
