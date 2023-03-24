#------------------------------------------------------------------------
import N10X

#------------------------------------------------------------------------
def ClangFormat(filename):
	os.system("clang-format -i " + filename)

#------------------------------------------------------------------------
# uncomment this line to format on save
#N10X.Editor.AddPostFileSaveFunction(ClangFormat)

