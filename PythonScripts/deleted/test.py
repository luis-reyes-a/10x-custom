import os
import sys
import subprocess

#------------------------------------------------------------------------
def Test():
	N10X.Editor.SaveAll()
	N10X.Editor.ClearBuildOutput()
	N10X.Editor.ShowBuildOutput()
	result = subprocess.run(["C:\\test.bat"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=False)
	N10X.Editor.LogToBuildOutput( result.stdout );
	N10X.Editor.LogToBuildOutput( result.stderr );
