#!/bin/bash

docker build --pull -t tensormarket/model_runner_server -f Dockerfile.build .
