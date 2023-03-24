#------------------------------------------------------------------------
import os
import N10X

Modal_Mode = False
Mark_Set = False
Set_Modal_Mode_After_Key_Intercept = False

def search_forward():
	if N10X.Editor.IsFindPanelOpen():
		#print("case 1")
		N10X.Editor.ExecuteCommand("FindInFileNext")
	else:
		#print("case 2")
		N10X.Editor.ExecuteCommand("FindInFile")
		
def insert_underscore():
	N10X.Editor.InsertText("_")
	
""" NOTE need some way to close tabs
def close_tab_or_panel():
	N10X.Editor.CloseFile();
	
"""
	
def toggle_cpp_header_source_file():
	filename = N10X.Editor.GetCurrentFilename()
	parts = os.path.splitext(filename)
	new_name = None;
	if parts[1] == '.h' or parts[1] == '.hpp':
		new_name = parts[0] + ".cpp"
	elif parts[1] == '.cpp' or parts[1] == '.c':
		new_name = parts[0] + ".h"
		
	if new_name is not None:
		N10X.Editor.OpenFile(new_name)

def select_line():
	cursor_pos = N10X.Editor.GetCursorPos()
	text = N10X.Editor.GetLine(cursor_pos[1])
	text_len = len(text)
	
	start_offset = 0
	for i in range(0, text_len):
		if (text[i] != ' ') and (text[i] != '\t'):
			start_offset = i
			break
	
	end_offset = 0
	for i in reversed(range(0, text_len)): 
		if (text[i] != ' ') and (text[i] != '\t') and (text[i] != '\n') and (text[i] != '\r'):
			end_offset = text_len - (i+1);
			break
			
	N10X.Editor.SetSelection((start_offset, cursor_pos[1]), (text_len-end_offset, cursor_pos[1]))
		
def toggle_autocomplete():
	if N10X.Editor.IsShowingAutocomplete():
		N10X.Editor.ExecuteCommand("CancelAutocomplete")
	else:
		N10X.Editor.ExecuteCommand("Autocomplete")
		
def search_backwards():
	if N10X.Editor.IsFindPanelOpen():
		N10X.Editor.ExecuteCommand("FindInFilePrev")
	else:
		N10X.Editor.ExecuteCommand("FindInFile")


def MoveToStartOfLine():
	cursor_pos = N10X.Editor.GetCursorPos()
	N10X.Editor.SetCursorPos((0, cursor_pos[1]))

def MoveToEndOfLine():
	cursor_pos = N10X.Editor.GetCursorPos()
	line = N10X.Editor.GetLine(cursor_pos[1])
	N10X.Editor.SetCursorPos((len(line), cursor_pos[1]))
	
def insert_underscore():
	N10X.Editor.InsertText("_")

#almost works but first line we're on gets shifted down...
def open_scope():
	N10X.Editor.SendKey("Enter")
	#N10X.Editor.InsertText("}")
	#N10X.Editor.ExecuteCommand("InsertLine")
	#N10X.Editor.SendKey("Tab")
	#N10X.Editor.ExecuteCommand("InsertLine")
	#N10X.Editor.InsertText("{")
	#N10X.Editor.ExecuteCommand("InsertLine")
	
	
	#N10X.Editor.SendKeyDown("Enter")
	#N10X.Editor.SendKeyUp("Enter")
	#N10X.Editor.InsertText("{")
	#N10X.Editor.SendKey("Enter")
	#N10X.Editor.SendKey("Tab")
	#N10X.Editor.SendKey("Enter")
	#N10X.Editor.InsertText("}")
	
def print_buffer_filename():
	name = N10X.Editor.GetCurrentFilename()
	print(name);

	
def build_active_workspace():
	N10X.Editor.ExecuteCommand("BuildActiveWorkspace")
	
	# BuildActiveWorkspace will show build panel in other view and not focus on it if it exists
	# if it doesn't exist, it makes it on the same panel, so we move it and move focus back
	
	show_build_output_other_panel()
			
def show_build_output_other_panel():
	N10X.Editor.ExecuteCommand("SetRowCount1")
	N10X.Editor.ExecuteCommand("SetColumnCount2")
	N10X.Editor.ExecuteCommand("ShowBuildOutput")
	
	filename = N10X.Editor.GetCurrentFilename() 
	if not filename: #note no way to check if current buffer is the buildpanel, so we just do it this way (will fail for other non-file panels)
		(grid_x, _) = N10X.Editor.GetCurrentPanelGridPos()
		if (grid_x == 0):
			N10X.Editor.ExecuteCommand("MovePanelRight")
			N10X.Editor.ExecuteCommand("MovePanelFocusLeft")
		else:
			N10X.Editor.ExecuteCommand("MovePanelLeft")
			N10X.Editor.ExecuteCommand("MovePanelFocusRight")
		

# NOTE taken from Example.py	
# Switches to single column and enables line numbers
def QuickPane1():
    N10X.Editor.ExecuteCommand("SetRowCount1")
    current=N10X.Editor.GetCurrentFilename()    # Temp workaround for current tab losing focus when SetColumnCount1 is called
    N10X.Editor.ExecuteCommand("SetColumnCount1")
    N10X.Editor.FocusFile(current)              # Temp workaround for current tab losing focus when SetColumnCount1 is called
    N10X.Editor.ExecuteCommand("CloseAllOtherTabs")
	
def QuickPane2():
	N10X.Editor.ExecuteCommand("SetRowCount1")
	# Only duplicate if right panel doesn't exist already
	(gridx, _) = N10X.Editor.GetCurrentPanelGridPos()
	if (gridx > 0): 
		return

	N10X.Editor.ExecuteCommand("DuplicatePanel")
	N10X.Editor.ExecuteCommand("MovePanelFocusRight")

	N10X.Editor.ExecuteCommand("SetColumnCount2")

	# If tthe panel was duplicated to the right column, we are done.
	(gridx, _) = N10X.Editor.GetCurrentPanelGridPos()
	if (gridx > 0): 
		return

	N10X.Editor.ExecuteCommand("MovePanelRight")
	return True
                                
# NOTE taken from Example.py									
# Switches to dual column and duplicates the current tab into the other panel.
def vsplit():
    # Only duplicate if right panel doesn't exist already
	column_count = N10X.Editor.GetColumnCount()
	if column_count > 1:
		return
	
	N10X.Editor.ExecuteCommand("SetRowCount1")

	N10X.Editor.ExecuteCommand("DuplicatePanel")
	N10X.Editor.ExecuteCommand("MovePanelFocusRight")

	N10X.Editor.ExecuteCommand("SetColumnCount2")

    # If tthe panel was duplicated to the right column, we are done.
	(gridx, _) = N10X.Editor.GetCurrentPanelGridPos()
	if (gridx > 0): return

	N10X.Editor.ExecuteCommand("MovePanelRight")
	return True
	
#really wish GotoSymbolDefinition() could just take in an argument asking to open in a differnt panel or make a new panel (if none)

def goto_symbol_same_panel():
	init_col_count = N10X.Editor.GetColumnCount()
	if init_col_count == 1: #if just one column, this will always work so we just abort here
		N10X.Editor.ExecuteCommand("GotoSymbolDefinition")
		return
		
	
	
	(init_grid_x, _) = N10X.Editor.GetCurrentPanelGridPos()
	#init_cursor_pos  = N10X.Editor.GetCursorPos()
	#init_filename    = N10X.Editor.GetCurrentFilename()
	
	
	N10X.Editor.ExecuteCommand("GotoSymbolDefinition")
	(new_grid_x, _) = N10X.Editor.GetCurrentPanelGridPos()
	
	grid_x = init_grid_x;
	while (grid_x < new_grid_x):
		N10X.Editor.ExecuteCommand("MovePanelRight")
		grid_x += 1;
		
	while (grid_x > new_grid_x):
		N10X.Editor.ExecuteCommand("MovePanelLeft")
		grid_x -= 1;
		

def goto_symbol_other_panel():
	N10X.Editor.ExecuteCommand("SetColumnCount2")
	
	init_cursor_pos = N10X.Editor.GetCursorPos()
	init_filename = N10X.Editor.GetCurrentFilename()
		
	(init_grid_x, _) = N10X.Editor.GetCurrentPanelGridPos()
	
	N10X.Editor.ExecuteCommand("GotoSymbolDefinition")
	new_filename = N10X.Editor.GetCurrentFilename();
	symbol_in_same_file = (new_filename == init_filename);
	if symbol_in_same_file:
		symbol_pos = N10X.Editor.GetCursorPos()
		N10X.Editor.ExecuteCommand("DuplicatePanel")
		N10X.Editor.SetCursorPos(symbol_pos)
		
	(new_grid_x, _)  = N10X.Editor.GetCurrentPanelGridPos()
	
	
	if new_grid_x == init_grid_x: # we're still on the same panel, we have to move it over one
		if init_grid_x == 0:
			N10X.Editor.ExecuteCommand("MovePanelRight")
			if symbol_in_same_file:
				N10X.Editor.ExecuteCommand("MovePanelFocusLeft")
				N10X.Editor.SetCursorPos(init_cursor_pos)
				N10X.Editor.ExecuteCommand("MovePanelFocusRight")
		else:
			N10X.Editor.ExecuteCommand("MovePanelLeft")
			if symbol_in_same_file:
				N10X.Editor.ExecuteCommand("MovePanelFocusRight")
				N10X.Editor.SetCursorPos(init_cursor_pos)
				N10X.Editor.ExecuteCommand("MovePanelFocusLeft")
	elif symbol_in_same_file: #here we duplicated a panel to the other side so we have to return initial panel to it's original cursor pos
		if new_grid_x == 0:
			N10X.Editor.ExecuteCommand("MovePanelFocusRight")
			N10X.Editor.SetCursorPos(init_cursor_pos)
			N10X.Editor.ExecuteCommand("MovePanelFocusLeft")
		else:
			N10X.Editor.ExecuteCommand("MovePanelFocusLeft")
			N10X.Editor.SetCursorPos(init_cursor_pos)
			N10X.Editor.ExecuteCommand("MovePanelFocusRight")

		
	
	
	
	
def cycle_panel_focus():
	(prev_grid_x, _) = N10X.Editor.GetCurrentPanelGridPos()
	N10X.Editor.ExecuteCommand("MovePanelFocusRight")
	(new_grid_x, _) = N10X.Editor.GetCurrentPanelGridPos()
	
	if new_grid_x == prev_grid_x:
		for i in range(new_grid_x):
			N10X.Editor.ExecuteCommand("MovePanelFocusLeft")
			
		
	


def swap_cursor_and_mark():
	(prev_cursor_x, prev_cursor_y) = N10X.Editor.GetCursorPos()
	(sel_start_x, sel_start_y)     = N10X.Editor.GetSelectionStart()
	(sel_end_x, sel_end_y)         = N10X.Editor.GetSelectionEnd()
	#print(f"Cursor {prev_cursor_x}, {prev_cursor_y} | {sel_start_x}, {sel_start_y} -> {sel_end_x}, {sel_end_y}")
	
	if   prev_cursor_x == sel_start_x and prev_cursor_y == sel_start_y: # move cursor to end of selection
		#print("case 1")
		N10X.Editor.ClearSelection()
		N10X.Editor.SetCursorPos((sel_start_x, sel_start_y))
		N10X.Editor.SetCursorPosSelect((sel_end_x, sel_end_y))
	elif prev_cursor_x == sel_end_x and prev_cursor_y == sel_end_y: # move cursor to start of selection
		#print("case 2")
		N10X.Editor.ClearSelection()
		N10X.Editor.SetCursorPos((sel_end_x, sel_end_y))
		N10X.Editor.SetCursorPosSelect((sel_start_x, sel_start_y))
	#else:
		#print("case 3")
		


#------------------------------------------------------------------------
# Called when a char is to be inserted into the text editor.
# Return true to surpress the char key.
def luis_intercept_char(c):
	global Modal_Mode
	global Mark_Set
	global Set_Modal_Mode_After_Key_Intercept
	#print(f"Char to intercept is {c}")
	if not Modal_Mode:
		return False;
	
	#else we're in modal mode so just do this and return true
	#if c == " ":
		#Mark_Set = not Mark_Set
	if c == "e" or c == "E":
		#N10X.Editor.ExecuteCommand("MoveCursorUp")
		Modal_Mode = False
		Set_Modal_Mode_After_Key_Intercept = True
		N10X.Editor.SendKey("Up", shift=Mark_Set)
			
	elif c == "d" or c == "D":
		#N10X.Editor.ExecuteCommand("MoveCursorDown")
		Modal_Mode = False
		Set_Modal_Mode_After_Key_Intercept = True
		N10X.Editor.SendKey("Down", shift=Mark_Set)
		
	elif c == "s" or c == "S":
		Modal_Mode = False
		Set_Modal_Mode_After_Key_Intercept = True
		N10X.Editor.SendKey("Left", shift=Mark_Set, control=True)
			
	elif c == "f" or c == "F":
		Modal_Mode = False
		Set_Modal_Mode_After_Key_Intercept = True
		N10X.Editor.SendKey("Right", shift=Mark_Set, control=True)

	elif c == "w" or c == "W":
		#N10X.Editor.ExecuteCommand("MoveCursorLeft")
		Modal_Mode = False
		Set_Modal_Mode_After_Key_Intercept = True
		N10X.Editor.SendKey("Left", shift=Mark_Set)
		
		
	elif c == "r" or c == "R":
		#N10X.Editor.ExecuteCommand("MoveCursorRight")
		Modal_Mode = False
		Set_Modal_Mode_After_Key_Intercept = True
		N10X.Editor.SendKey("Right", shift=Mark_Set)
		
	elif c == "a" or c == "A":
		Modal_Mode = False
		Set_Modal_Mode_After_Key_Intercept = True
		N10X.Editor.SendKey("Home", shift=Mark_Set)
		
	elif c == "g" or c == "G":
		Modal_Mode = False
		Set_Modal_Mode_After_Key_Intercept = True
		N10X.Editor.SendKey("End", shift=Mark_Set)
	
	elif c == "c" or c == "C":
		N10X.Editor.ExecuteCommand("Copy")
		Mark_Set = False
		N10X.Editor.ClearSelection()
		
	elif c == "x" or c == "X":
		N10X.Editor.ExecuteCommand("Cut")
		Mark_Set = False
		N10X.Editor.ClearSelection()
		
	elif c == "k" or c == "K":
		select_line()
		
	elif c == "v" or c == "V":
		N10X.Editor.ExecuteCommand("Paste")	
		
	elif c == "u" or c == "U": #redo is ctrl+U
		N10X.Editor.ExecuteCommand("Undo")	
		
	elif c == "\'":
		Mark_Set = True
		#this way doesn't work (I expect it's because cursor doesn't get updated immediately?)
		#N10X.Editor.ExecuteCommand("MoveCursorLeft")
		
		original_sel_start = N10X.Editor.GetSelectionStart();
		original_sel_end   = N10X.Editor.GetSelectionEnd();
		original_sel_ydelta = original_sel_end[1] - original_sel_start[1];
		
		
		#swap_cursor_and_mark() //doesn't work if move around and attempt to fix again
		(cx, cy) = N10X.Editor.GetCursorPos();
		N10X.Editor.SetCursorPos((cx-1, cy));
		
		N10X.Editor.ExecuteCommand("SelectCurrentScope")
		swap_cursor_and_mark()
		
		# note prob the best way to do this is to call SelectCurrentScope twice, once at current pos and one one to the left
		# and just select the bigger selection region, however we don't have a way to compare selections ranges for their size...
		# my method will work but not if the braces rest on the same line like {{{ }}}
		new_sel_start = N10X.Editor.GetSelectionStart();
		new_sel_end   = N10X.Editor.GetSelectionEnd();
		new_sel_ydelta = new_sel_end[1] - new_sel_start[1];
		if (new_sel_ydelta < original_sel_ydelta):
			N10X.Editor.SetCursorPos(original_sel_start);
			N10X.Editor.SetCursorPosSelect(original_sel_end);
	
	elif c == "/":
		N10X.Editor.ExecuteCommand("ToggleComment")
		
        
	return True

#------------------------------------------------------------------------
# Called when a key is pressed.
# Return true to surpress the key
def luis_intercept_key(key, shift, control, alt):
	global Modal_Mode
	global Mark_Set
	global Set_Modal_Mode_After_Key_Intercept
	
	
	if key == "D" and control == True:
		Modal_Mode = not Modal_Mode
		if Modal_Mode:
			N10X.Editor.SetCursorColourOverride((255, 0, 0))
			N10X.Editor.ResetCursorBlink()
		else:
			N10X.Editor.ClearCursorColourOverride()
			N10X.Editor.ResetCursorBlink()
			#clear selections if any
			Mark_Set = False
			N10X.Editor.ClearSelection()
		return True
	elif key == "F" and control:
		search_forward()
		return True
	elif key == "R" and control:
		search_backwards()
		return True
	elif key == "Q" and control:
		N10X.Editor.ExecuteCommand("FindReplaceInFile")
		return True
	elif key == "T" and control:
		toggle_cpp_header_source_file();
		return True
	elif key == "C" and control:
		N10X.Editor.ExecuteCommand("Copy")
		Mark_Set = False
		N10X.Editor.ClearSelection()
		return True
	elif key == "/" and control:
		N10X.Editor.ExecuteCommand("ToggleComment")
		return True
	elif key == "`" and control:
		N10X.Editor.ExecuteCommand("ToggleWorkspaceExplorer")
		return True
	elif key == "," and control:
		N10X.Editor.ExecuteCommand("insert_underscore")
		return True
	elif key == "." and control:
		N10X.Editor.InsertText("->")
		return True
	elif key == "I" and control:
		#N10X.Editor.InsertText("{")
		N10X.Editor.SendCharKey("{")
		N10X.Editor.SendKey("Enter")
		N10X.Editor.SendKey("Enter")
		N10X.Editor.SendCharKey("}")
		N10X.Editor.SendKey("Up")
		N10X.Editor.SendKey("Tab")
		
		return True
	elif key == ";" and control:
		cycle_panel_focus()
		return True
	elif key == "Enter":
		if N10X.Editor.IsFindPanelOpen():
			N10X.Editor.SendKey("Escape")
			return True
	elif key == "J" and control:
		if N10X.Editor.IsShowingAutocomplete():
			N10X.Editor.SendKey("Enter")
			return True
	elif key == "K" and control:
		if N10X.Editor.IsShowingAutocomplete():
			N10X.Editor.SendKey("Down")
			return True
		else:
			select_line()
	elif key == "L" and control:
		if N10X.Editor.IsShowingAutocomplete():
			N10X.Editor.SendKey("Up")
			return True
		else:
			(cx, cy) = N10X.Editor.GetCursorPos();
			N10X.Editor.CenterViewAtLinePos(cy+4);
			
	elif key == "Down" and alt:
		if control:
			goto_symbol_same_panel()
		else:
			goto_symbol_other_panel()
			
	elif key == "Left":
		if alt:
			if control:
				N10X.Editor.ExecuteCommand("PrevLocation")
				return True
			else:
				N10X.Editor.ExecuteCommand("PrevLocationCurrentFile")
				return True
				
	elif key == "Right":
		if alt:
			if control:
				N10X.Editor.ExecuteCommand("NextLocation")
				return True
			else:
				N10X.Editor.ExecuteCommand("NextLocationCurrentFile")
				return True
			
			
	
	
		
		
		
		
		
	
	if Modal_Mode:
		if key == "Space":
			if control == True:
				swap_cursor_and_mark()
			else:
				Mark_Set = not Mark_Set
				if not Mark_Set:
					N10X.Editor.ClearSelection()
		elif key == "U" and control:
			N10X.Editor.ExecuteCommand("Redo")
		elif key == "Tab":
			if control:
				N10X.Editor.ExecuteCommand("UnindentLine")
			else:
				N10X.Editor.ExecuteCommand("IndentLine")
		elif key == "Backspace" or key == "Enter": #bypass these guys
			Mark_Set = False;
			return False
		
		return True
		
		
	# NOTE hacky thing we have to do to make selecting upwards/downards work since there isn't a command for that...
	if Set_Modal_Mode_After_Key_Intercept:
		Set_Modal_Mode_After_Key_Intercept = False
		Modal_Mode = True
		
	return False

#------------------------------------------------------------------------
def luis_init():
	print("Hello intercept")
	N10X.Editor.AddOnInterceptCharKeyFunction(luis_intercept_char)
	N10X.Editor.AddOnInterceptKeyFunction(luis_intercept_key)

N10X.Editor.CallOnMainThread(luis_init)
#N10X.Editor.AddUpdateFunction(Initialize)