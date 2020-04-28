#!/bin/bash
currentDir = $PWD
cd "$(dirname "$0")"
docker build -t rsbyrne/fbapi:latest .
docker push rsbyrne/fbapi:latest
cd $currentDir
