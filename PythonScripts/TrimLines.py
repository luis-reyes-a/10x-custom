#------------------------------------------------------------------------
import N10X

#------------------------------------------------------------------------
def TrimLines(fn):
    N10X.Editor.PushUndoGroup()
    N10X.Editor.BeginTextUpdate()

    line_count = N10X.Editor.GetLineCount()

    for i in range(line_count):
        line = N10X.Editor.GetLine(i)
        line = line.rstrip()
        N10X.Editor.SetLine(i, line)

    N10X.Editor.EndTextUpdate()
    N10X.Editor.PopUndoGroup()
	
#------------------------------------------------------------------------
# uncomment this line to trim on save
#N10X.Editor.AddPreFileSaveFunction(TrimLines)

