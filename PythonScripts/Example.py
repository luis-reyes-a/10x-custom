#------------------------------------------------------------------------
import N10X

#------------------------------------------------------------------------
# this function is bound to Alt-H and prints "Hello World!" to the 10x Output window
def HelloWorld():
	print("Hello World!");

#------------------------------------------------------------------------
def ToggleColumnCount():
	column_count = N10X.Editor.GetColumnCount()
	if column_count == 1:
		column_count = 2
	else:
		column_count = 1
	N10X.Editor.SetColumnCount(column_count)
		
#------------------------------------------------------------------------
# shows how to use the N10X interface to insert text in the current text editor
def InsertText():
	N10X.Editor.InsertText("Hello 10x")

