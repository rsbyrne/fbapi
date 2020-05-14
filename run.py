import sys

import code

filepath = sys.argv[0]
dataURL = sys.argv[1]
loginName = sys.argv[2]
loginPass = sys.argv[3]
outDir = sys.argv[4]
dataMime = sys.argv[5]
outExt = sys.argv[6]

code.pull_datas(dataURL, loginName, loginPass, outDir, dataMime, outExt)
