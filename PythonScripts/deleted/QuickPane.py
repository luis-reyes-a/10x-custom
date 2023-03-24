#------------------------------------------------------------------------
import os
import N10X

#------------------------------------------------------------------------
# This script tries to simulate vim's "vsplit" and "only" commands
# for 2 panes. I.e. "split current window into 2 panes and duplicate current
# buffer to the other pane" and "only one pane, with current buffer"

# Stick this file in your 10x PythonScripts folder,
# typically \users\USERNAME\AppData\Roaming\10x\PythonScripts
# For this to work, please map two keys to QuickPane1() and QuickPane2() in
# key bindings (KeyMappings.10x_settings). F1 and F2 are recommended,
# but they need to be unmapped from other uses first!

#------------------------------------------------------------------------
# Switches to single column and enables line numbers
def QuickPane1():
    N10X.Editor.ExecuteCommand("SetRowCount1")
    current=N10X.Editor.GetCurrentFilename()    # Temp workaround for current tab losing focus when SetColumnCount1 is called
    N10X.Editor.ExecuteCommand("SetColumnCount1")
    N10X.Editor.FocusFile(current)              # Temp workaround for current tab losing focus when SetColumnCount1 is called
    N10X.Editor.ExecuteCommand("CloseAllOtherTabs")
                                                        
# Switches to dual column and duplicates the current tab into the other panel.
def QuickPane2():
    N10X.Editor.ExecuteCommand("SetRowCount1")
    # Only duplicate if right panel doesn't exist already
    (gridx, _) = N10X.Editor.GetCurrentPanelGridPos()
    if (gridx > 0): return

    N10X.Editor.ExecuteCommand("DuplicatePanel")
    N10X.Editor.ExecuteCommand("MovePanelFocusRight")

    N10X.Editor.ExecuteCommand("SetColumnCount2")

    # If tthe panel was duplicated to the right column, we are done.
    (gridx, _) = N10X.Editor.GetCurrentPanelGridPos()
    if (gridx > 0): return

    N10X.Editor.ExecuteCommand("MovePanelRight")
    return True