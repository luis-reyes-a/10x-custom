import N10X

def _set_show_line_numbers(show):
  N10X.Editor.SetSetting("Editor.Line Numbers", "true" if show else "false")
  N10X.Editor.SetSetting("UI.MapScrollBarWidth", "80" if show else "40")
  N10X.Editor.CheckForModifiedFiles()


def _select_tab(filename):
  if(not filename): return

  previous_file = 0

  while(1):
    check_file = N10X.Editor.GetCurrentFilename()
    if (check_file == filename or check_file == previous_file): return
    previous_file = check_file
    N10X.Editor.ExecuteCommand("PrevPanelTab")


def DualPanel():
  current_file = N10X.Editor.GetCurrentFilename()
  N10X.Editor.ExecuteCommand("SetColumnCount2")
  N10X.Editor.ExecuteCommand("ToggleWorkspaceExplorer")
  _set_show_line_numbers(False)


  if (N10X.Editor.GetCurrentFilename() != current_file):
    N10X.Editor.ExecuteCommand("MovePanelFocusRight")
    _select_tab(current_file)


def SinglePanel():
  current_file = N10X.Editor.GetCurrentFilename()
  N10X.Editor.ExecuteCommand("SetColumnCount1")
  _set_show_line_numbers(True)
  _select_tab(current_file)
  N10X.Editor.ExecuteCommand("ShowInWorkspaceTree")

