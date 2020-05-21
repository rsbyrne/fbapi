#!/bin/bash
currentDir=$PWD
cd "$(dirname "$0")"
git add .
git commit -m "Automatic push."
git fetch
git merge
git push
docker build -t rsbyrne/fbapi:latest .
docker push rsbyrne/fbapi:latest
cd $currentDir
