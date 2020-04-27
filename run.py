import sys

from .code import pull_datas

filepath = sys.argv[0]
dataURL = sys.argv[1]
loginName = sys.argv[2]
loginPass = sys.argv[3]
outDir = sys.argv[4]
dataMime = sys.argv[5]
outExt = sys.argv[6]

pull_datas(dataURL, loginName, loginPass, dataMime, outDir, outExt)
