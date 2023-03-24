#------------------------------------------------------------------------
def FormatFile():
    N10X.Editor.SaveFile()
    import subprocess
    process = subprocess.Popen(['clang-format.exe',
                                 '-style=file',
                                 '-i',
                                 N10X.Editor.GetCurrentFilename()],
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    N10X.Editor.CheckForModifiedFiles()

