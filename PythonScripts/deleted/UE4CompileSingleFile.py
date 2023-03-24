#------------------------------------------------------------------------
# Copyright (c) 2021 Nuno Leiria
# MIT License (MIT) <http://opensource.org/licenses/MIT>
#------------------------------------------------------------------------

import N10X
import subprocess
import threading
import os

#------------------------------------------------------------------------
def find_build_bat(active_project):

	# first try getting it from the active project file <NMakeBuildCommandLine>

	file = open(active_project, "rt")
	lines = file.readlines()
	file.close()

	for line in lines:
		nmake_index = line.find("<NMakeBuildCommandLine>")
		build_bat_index = line.find("Build.bat")
		
		if nmake_index != -1 and build_bat_index != -1:
			build_bat = line[nmake_index + len("<NMakeBuildCommandLine>") : build_bat_index + len("Build.bat")]
			build_bat = os.path.abspath(build_bat)
			if os.path.exists(build_bat):
				return build_bat

	# try getting it from the UnrealBuildTool path

	project_files = N10X.Editor.GetWorkspaceProjectFiles()
	unreal_build_tool_proj = None
	for file in project_files:
		if file.find("/UnrealBuildTool.csproj") != -1:
			unreal_build_tool_proj = file
			break

	if unreal_build_tool_proj:
		unreal_build_tool_proj_dir = os.path.dirname(unreal_build_tool_proj)
		build_bat = os.path.abspath(os.path.join(unreal_build_tool_proj_dir, "../../../Build/BatchFiles/Build.bat"))
		if os.path.exists(build_bat):
			return build_bat

	N10X.Editor.LogToBuildOutput("ERROR: unable to find Build.bat path\n")
	return None

#------------------------------------------------------------------------
def compile_async(current_file, workspace_filename, active_project, build_platform, build_config, batch_file):

	slash_index = active_project.rfind('/') + 1
	dot_index = active_project.rfind('.')
	
	N10X.Editor.LogToBuildOutput("Compiling SingleFile " + current_file + "\n")

	uproject_filename = os.path.splitext(workspace_filename)[0] + ".uproject"
	working_dir = os.path.dirname(batch_file)

	command = "\"" + batch_file + "\" " + active_project[slash_index:dot_index] + " \"" \
		+ build_platform + "\" \"" + build_config + "\" -SingleFile=" + current_file + \
		" \"" + uproject_filename + "\""

	N10X.Editor.LogToBuildOutput("command: " + command + "\n")

	output = subprocess.Popen(
		command, 
		cwd=working_dir,
		text=True,
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		close_fds=True,
		shell=True)

	while True:
		line = output.stdout.readline()
		if not line:
			break
		N10X.Editor.LogToBuildOutput(line)    	

	output.kill()

#------------------------------------------------------------------------
def UE_Compile_Single_File():
	N10X.Editor.ShowBuildOutput()
	current_file = N10X.Editor.GetCurrentFilename()
	if not current_file:
		N10X.Editor.LogToBuildOutput("Trying to compile a SingleFile without specifying a valid file\n")
		return

	workspace_filename = N10X.Editor.GetWorkspaceFilename()
	active_project = N10X.Editor.GetActiveProject()
	build_config = N10X.Editor.GetBuildConfig()
	build_platform = N10X.Editor.GetBuildPlatform()

	if "Debug" in build_config:			build_config = "Debug"
	if "Development" in build_config:	build_config = "Development"
	if "Shipping" in build_config:		build_config = "Shipping"
	if "Test" in build_config:			build_config = "Test"

	batch_file = find_build_bat(active_project)
	if not batch_file:
		return

	async_job = threading.Thread(target=compile_async, args=(current_file, workspace_filename, active_project, build_platform, build_config, batch_file))
	async_job.start()
