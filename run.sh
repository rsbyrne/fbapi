#!/bin/bash
dataURL=$1
loginName=$2
loginPass=$3
outDir=${4:-$PWD}
dataMime=${5:-'text/csv'}
outExt=${6:-'.csv'}
MOUNTFROM=$outDir
MOUNTTO='/mnt'
IMAGE='rsbyrne/fbapi'
SCRIPTPATH='/fbapi/run.py'
mkdir -p $outDir
docker run -v $MOUNTFROM:$MOUNTTO -it --shm-size 2g $IMAGE \
  python $SCRIPTPATH $dataURL $loginName $loginPass $MOUNTTO $dataMime $outExt
