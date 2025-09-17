#! /usr/bin/env bash

docker run -p 11235:11235 -it --rm oe-base/crawl4ai --shm-size=1g
