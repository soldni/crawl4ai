#! /usr/bin/env bash

docker run -p 11235:11235 --shm-size=1g -it --rm oe-base/crawl4ai
