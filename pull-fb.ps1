$dataURL = $args[0]
$loginName = $args[1]
$loginPass = $args[2]
$outDir = $args[3]
$dataMime = 'text/csv'
$outExt = '.csv'
$MOUNTFROM = $outDir
$MOUNTTO = '/mnt'
$IMAGE = 'rsbyrne/fbapi'
$SCRIPTPATH = '/fbapi/run.py'
New-Item -ItemType Directory -Force -Path $outDir
docker run -v ${MOUNTFROM}:${MOUNTTO} -it --shm-size 2g $IMAGE python $SCRIPTPATH $dataURL $loginName $loginPass $MOUNTTO $dataMime $outExt
echo 'Done.'
