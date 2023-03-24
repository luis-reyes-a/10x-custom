#------------------------------------------------------------------------
import N10X

#------------------------------------------------------------------------
def SortLines():

	lines = []
	line_count = N10X.Editor.GetLineCount()

	for i in range(line_count):
		lines.append(N10X.Editor.GetLine(i))

	lines.sort()

	for i in range(line_count):
		N10X.Editor.SetLine(i, lines[i])
	
	