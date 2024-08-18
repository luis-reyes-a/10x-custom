import N10X

g_mark_pos = (0, 0)
g_pos_when_started_incremental_search = (0, 0)
g_escape_pressed_when_doing_incremental_search = False
g_enter_pressed_when_doing_incremental_search = False

def luis_intercept_key(key, shift, control, alt):
	global g_escape_pressed_when_doing_incremental_search
	global g_enter_pressed_when_doing_incremental_search
	# global g_pos_when_started_incremental_search
	if key == "Escape":
		if N10X.Editor.IsFindPanelOpen():
			g_escape_pressed_when_doing_incremental_search = True
			
	if key == "Enter":
		if N10X.Editor.IsFindPanelOpen():
			N10X.Editor.SendKey("Escape") # will this go back to message loop?
			g_enter_pressed_when_doing_incremental_search = True
		
	return False

	
"""
def luis_on_key(key, shift, control, alt):
	global g_escape_pressed_when_doing_incremental_search
	global g_pos_when_started_incremental_search
	if key == "Escape":
		print (f"ESC pressed and bool is {g_escape_pressed_when_doing_incremental_search}")
		if g_escape_pressed_when_doing_incremental_search:
			g_escape_pressed_when_doing_incremental_search = False
			N10X.Editor.SetCursorPos(g_pos_when_started_incremental_search)
			print (f"Tried to set cursor pos to {g_pos_when_started_incremental_search}")
		if N10X.Editor.IsFindPanelOpen():
			print ("Escape still searching?")
		else:
			print ("Escape NO SEARCHING")
"""		


def luis_update():
	global g_escape_pressed_when_doing_incremental_search
	global g_enter_pressed_when_doing_incremental_search
	global g_pos_when_started_incremental_search
	if g_escape_pressed_when_doing_incremental_search:
			g_escape_pressed_when_doing_incremental_search = False
			if g_enter_pressed_when_doing_incremental_search:
				g_enter_pressed_when_doing_incremental_search = False
				# do nothing
			else:
				N10X.Editor.SetCursorPos(g_pos_when_started_incremental_search)
	

def luis_init():
	N10X.Editor.AddOnInterceptKeyFunction(luis_intercept_key)
	#N10X.Editor.AddOnKeyFunction(luis_on_key)
	N10X.Editor.AddUpdateFunction(luis_update)

N10X.Editor.CallOnMainThread(luis_init)

def emacs_set_mark():
	global g_mark_pos
	g_mark_pos = N10X.Editor.GetCursorPos()

def search_forward():
	global g_pos_when_started_incremental_search
	if N10X.Editor.IsFindPanelOpen():
		N10X.Editor.ExecuteCommand("FindInFileNext")
	else:
		g_pos_when_started_incremental_search = N10X.Editor.GetCursorPos()
		# N10X.Editor.ExecuteCommand("ClearAllBookmarks")
		# N10X.Editor.ExecuteCommand("ToggleBookmark")
		N10X.Editor.ExecuteCommand("FindInFile")

def search_backwards():
	global g_pos_when_started_incremental_search
	if N10X.Editor.IsFindPanelOpen():
		N10X.Editor.ExecuteCommand("FindInFilePrev")
	else:
		g_pos_when_started_incremental_search = N10X.Editor.GetCursorPos()
		# N10X.Editor.ExecuteCommand("ClearAllBookmarks")
		# N10X.Editor.ExecuteCommand("ToggleBookmark")
		N10X.Editor.ExecuteCommand("FindInFile")
		
def emacs_kill_line():
	N10X.Editor.ExecuteCommand("SelectToLineEnd")
	N10X.Editor.ExecuteCommand("Cut")
	
def emacs_copy():
	global g_mark_pos
	N10X.Editor.ExecuteCommand("Copy")
	(cursor_pos, other_pos) = get_selection_cursor_pos_and_other_end()
	g_mark_pos = other_pos;
	N10X.Editor.SendKey("Escape")
	

# dones't work to well, I think it's some bug with cursor pos being an (x, y) instead of a byte offset...
def emacs_paste():
	emacs_set_mark()
	N10X.Editor.ExecuteCommand("Paste")
	
def is_pos_before(p1, p2):
	if p1[1] < p2[1]: 
		return True
	elif p1[1] > p2[1]:
		return False
	elif p1[0] < p2[0]:
		return True;
	elif p1[0] > p2[0]:
		return False
	return False
	
# taken from staniw from 10x discord
def ReverseSelection():
	(cur_x, cur_y) = N10X.Editor.GetCursorPos()
	(start_x, start_y) = N10X.Editor.GetSelectionStart()
	(end_x, end_y) = N10X.Editor.GetSelectionEnd()
	if (cur_x, cur_y) == (start_x, start_y):
		N10X.Editor.SetCursorPos((end_x, end_y))
		N10X.Editor.SetSelection((start_x, start_y), (end_x, end_y))
	else:
		N10X.Editor.SetCursorPos((start_x, start_y))
		N10X.Editor.SetSelection((end_x, end_y), (start_x, start_y))
		
def is_there_selection(cursor_index = 0):
	(p1x,p1y), (p2x,p2y) = N10X.Editor.GetCursorSelection();
	return (p1x, p1y) != (p2x, p2y)
	
def get_selection_cursor_pos_and_other_end():
	(cur_x, cur_y)     = N10X.Editor.GetCursorPos()
	(start_x, start_y) = N10X.Editor.GetSelectionStart()
	(end_x, end_y)     = N10X.Editor.GetSelectionEnd()
	if (cur_x, cur_y) == (start_x, start_y):
		return ((cur_x, cur_y), (end_x, end_y))
	else:
		return ((cur_x, cur_y), (start_x, start_y))
	
def emacs_swap_cursor_mark():
	global g_mark_pos
	if is_there_selection():
		ReverseSelection()
		(cursor_pos, other_pos) = get_selection_cursor_pos_and_other_end()
		g_mark_pos = other_pos;
	elif g_mark_pos != N10X.Editor.GetCursorPos():
		init_cursor_pos = N10X.Editor.GetCursorPos()
		N10X.Editor.SetSelection(g_mark_pos, init_cursor_pos)
		(cursor_pos, other_pos) = get_selection_cursor_pos_and_other_end();
		if (cursor_pos == init_cursor_pos):
			g_mark_pos = init_cursor_pos
			ReverseSelection();
		else:
			g_mark_pos = other_pos
	#else : in emacs this sets the cursor and begins selection mode, we can't quite do that yet...
	

	
def select_surrounding_scope():
	if is_there_selection():
		ReverseSelection()	
	N10X.Editor.ExecuteCommand("SelectCurrentScope")
	ReverseSelection();
	


	
	
	
# stolen from 10x/python scripts on github
def GetLine(y=None):
	if y is None:
		x, y = N10X.Editor.GetCursorPos()
	return N10X.Editor.GetLine(y)

def GetLineLength(y=None):
	line = GetLine(y)
	line = line.rstrip("\r\n")
	return len(line)

def GetMaxY():
	return max(0, N10X.Editor.GetLineCount() - 1)

def AtEndOfFile(x, y):
	return y > GetMaxY() or (y == GetMaxY() and x >= GetLineLength(GetMaxY()))
	
def IsWhitespaceChar(c):
	return c == ' ' or c == '\t' or c == '\r' or c == '\n'

def IsWhitespace(x, y):
	line = GetLine(y)
	return x >= len(line) or IsWhitespaceChar(line[x])
	
def GetNextNonWhitespaceCharPos(x, y, wrap=True):
	while not AtEndOfFile(x, y) and IsWhitespace(x, y):
		if x >= GetLineLength(y):
			if wrap and y < GetMaxY():
				x = 0
				y += 1
			else:
				break
		else:
			x += 1
	return x, y

def MoveToNextNonWhitespaceChar(wrap=True):
	x, y = N10X.Editor.GetCursorPos()
	end_x, end_y = GetNextNonWhitespaceCharPos(x, y, wrap)
	N10X.Editor.SetCursorPos((end_x, end_y))
	print("move right")


	
def GetPrevNonWhitespaceCharPos(x, y):
	while y and IsWhitespace(x, y):
		if x == 0:
			y -= 1
			x = GetLineLength(y)
			if x:
				x -= 1
		else:
			x -= 1
	return x, y
	

# close all panels except this one
def emacs_cx_1():
	(gridx, gridy) = N10X.Editor.GetCurrentPanelGridPos() # 0 based
	print (f"{gridx} and {gridy}");
	for i in range(gridx):
		N10X.Editor.ExecuteCommand("MovePanelLeft")
		
	for i in range(gridy):
		N10X.Editor.ExecuteCommand("MovePanelUp")
		
	N10X.Editor.ExecuteCommand("SetRowCount1")
	N10X.Editor.ExecuteCommand("SetColumnCount1")
	
def emacs_cx_3():
	(gridx, gridy) = N10X.Editor.GetCurrentPanelGridPos() 
	if gridx > 0:
		N10X.Editor.ExecuteCommand("DuplicatePanelLeft")
		return
		
	N10X.Editor.ExecuteCommand("SetColumnCount2")
	(gridx, gridy) = N10X.Editor.GetCurrentPanelGridPos() 
	if gridx > 0: 
		N10X.Editor.ExecuteCommand("DuplicatePanelLeft")
		N10X.Editor.ExecuteCommand("MovePanelFocusRight")
		# means we were on a panel that belonged to next column, callling SetColumnCount2 moved us already there
		return
		
	# here we didn't move, so let's just move
	N10X.Editor.ExecuteCommand("DuplicatePanelRight")
	
def focus_next_panel():
	(gridx, gridy) = N10X.Editor.GetCurrentPanelGridPos() 
	if gridx == 0:
		N10X.Editor.ExecuteCommand("MovePanelFocusRight")
	else:
		N10X.Editor.ExecuteCommand("MovePanelFocusLeft")
		
# TODO this only works with two columns active
def emacs_cx_0():
	focus_next_panel();
	emacs_cx_1();
	
def toggle_header_source_file_other_view():
	emacs_cx_3();
	N10X.Editor.ExecuteCommand("CppParser.ToggleSourceHeader")
	
	










def MoveToPrevNonWhitespaceChar():
	x, y = N10X.Editor.GetCursorPos()
	end_x, end_y = GetPrevNonWhitespaceCharPos(x, y)
	N10X.Editor.SetCursorPos((end_x, end_y))
	print("move left")
	
class CharacterClass:
	WHITESPACE  = 0
	DEFAULT     = 1
	WORD        = 2
	
def GetCharacterClass(c):
	if IsWordChar(c):
		return CharacterClass.WORD
	if IsWhitespaceChar(c):
		return CharacterClass.WHITESPACE
	return CharacterClass.DEFAULT

#------------------------------------------------------------------------
def GetCharacterClassAtPos(x, y):
	line = GetLine(y)
	return GetCharacterClass(line[x]) if x < len(line)  else CharacterClass.WHITESPACE

#------------------------------------------------------------------------


def IsWordChar(c):
	return \
		(c >= 'a' and c <= 'z') or \
		(c >= 'A' and c <= 'Z') or \
		(c >= '0' and c <= '9') or \
		c == '_'

#------------------------------------------------------------------------
def IsWord(x, y):
	line = GetLine(y)
	return IsWordChar(line[x])

def GetPrevCharPos(x, y):
	if x:
		x -= 1
	elif y:
		y -= 1
		x = max(0, GetLineLength(y) - 1)
	else:
		x = 0
		y = 0
	return x, y
	
def GetWordStart():
	x, y = N10X.Editor.GetCursorPos()

	x, y = GetPrevCharPos(x, y)
	x, y = GetPrevNonWhitespaceCharPos(x, y)

	line = N10X.Editor.GetLine(y)

	if x < len(line):
		character_class = GetCharacterClass(line[x])
		while x > 0:
			if GetCharacterClass(line[x - 1]) != character_class:
				break
			x -= 1

	return x, y

#------------------------------------------------------------------------
def MoveToWordStart():
	new_x, new_y = GetWordStart()
	N10X.Editor.SetCursorPos((new_x, new_y))
	
def GetNextCharPos(x, y, wrap=True):
	if x < GetLineLength(y):
		x += 1
	if wrap and x >= GetLineLength(y) and y < GetMaxY():
		x = 0
		y += 1
	return x, y

	
	
def GetWordEndPos(x, y, wrap=True):
	x, y = N10X.Editor.GetCursorPos()

	x, y = GetNextCharPos(x, y, wrap)
	x, y = GetNextNonWhitespaceCharPos(x, y, wrap)

	line = N10X.Editor.GetLine(y)

	if x < len(line):
		character_class = GetCharacterClass(line[x])
		while x < len(line):
			if GetCharacterClass(line[x]) != character_class:
				break
			x += 1
	if x:
		x -= 1
	# NOTE(LUIS) added +1 to x since vim likes to make selections include where cursor is at...ughh
	return x+1, y 

def MoveToWordEnd():
	x, y = N10X.Editor.GetCursorPos()
	new_x, new_y = GetWordEndPos(x, y)
	N10X.Editor.SetCursorPos((new_x, new_y))
	




def open_up_braces():
	x, y = N10X.Editor.GetCursorPos()
	line = GetLine(y)
	moved_cursor_to_open_brace = False
	while x >= 0:
		if line[x] == '}':
			N10X.Editor.SetCursorPos((x, y))
			moved_cursor_to_open_brace = True
			break
		x -= 1;
	
	if moved_cursor_to_open_brace:
		N10X.Editor.InsertText('\n')
		N10X.Editor.InsertText('\n')
		N10X.Editor.SendKey("Up")
		N10X.Editor.InsertText('\t')	
	

# Neither of these write_open_braces work well (they don't indent last brace preoperly for whatever reason	
"""
def write_open_braces():
	N10X.Editor.InsertText('{}')
	N10X.Editor.SendKey("Left")
	N10X.Editor.InsertText('\n')
	N10X.Editor.InsertText('\n')
	N10X.Editor.SendKey("Up")
	N10X.Editor.InsertText('\t')	

"""
def write_open_braces():
	N10X.Editor.InsertText("{} ")
	open_up_braces()

"""
def is_at_word_separator(x, y):
	line = GetLine(y)
	if x >= len(line):
		return True # assume it's a newline
	c = line[x]
	return  (c == ' ' or c == '\t' or c == '\r' or c == '\n' or
	c == '[' or c == '(' or c == ')' or c == ']' or c == ',')
	
"""

def is_at_word_separator(x, y):
	line = GetLine(y)
	if x >= len(line):
		return True # assume it's a newline
	c = line[x]
	return not (c.isalnum() or c == '_')


def move_next_word_boundary_pos():
	x, y     = N10X.Editor.GetCursorPos()
	hit_word = False
	while not AtEndOfFile(x, y):
		if is_at_word_separator(x, y):
			if hit_word:
				break;
		else:
			hit_word = True
		
		x += 1
		if x > GetLineLength(y):
			if y < GetMaxY():
				x = 0
				y += 1
			else:
				break
	
	return (x, y)
	

def get_pos_before_pos(x, y):
	if x > 0:
		return (x - 1, y)
		
	y -= 1
	if (y >= 0):
		x = GetLineLength(y)
	else:
		y = 0
	return (x, y)
		
		
		
	
def move_prev_word_boundary_pos():
	#N10X.Editor.ExecuteCommand("MoveCursorLeft")
	x, y = N10X.Editor.GetCursorPos()
	x, y = get_pos_before_pos(x, y)  
	# we want last pos when hit_word was set to true
	(last_x, last_y) = (x, y)
	hit_word = False
	while y >= 0:
		if is_at_word_separator(x, y):
			if hit_word:
				break;
		else:
			hit_word = True
		
		last_x = x
		last_y = y
		
		if x == 0:
			y -= 1;
			x = GetLineLength(y)
			#if x:
				#x -= 1
		else:
			x -= 1;
	
	return (last_x, last_y)
	
def move_next_word_boundary():
	N10X.Editor.SetCursorPos(move_next_word_boundary_pos())

def move_prev_word_boundary():
	N10X.Editor.SetCursorPos(move_prev_word_boundary_pos())



def move_prev_word_boundary_select():
	(init_cursor_pos, init_other_pos) = get_selection_cursor_pos_and_other_end()
	new_cursor_pos = move_prev_word_boundary_pos()
	N10X.Editor.SetSelection(init_other_pos, new_cursor_pos)	
	
def move_next_word_boundary_select():
	(init_cursor_pos, init_other_pos) = get_selection_cursor_pos_and_other_end()
	new_cursor_pos = move_next_word_boundary_pos()
	N10X.Editor.SetSelection(init_other_pos, new_cursor_pos)

def delete_to_prev_word_boundary():
	(init_cursor_pos, init_other_pos) = get_selection_cursor_pos_and_other_end()
	new_cursor_pos = move_prev_word_boundary_pos()
	N10X.Editor.SetSelection(init_other_pos, new_cursor_pos)
	N10X.Editor.ExecuteCommand("Delete")

def delete_to_next_word_boundary():
	(init_cursor_pos, init_other_pos) = get_selection_cursor_pos_and_other_end()
	new_cursor_pos = move_next_word_boundary_pos()
	N10X.Editor.SetSelection(init_other_pos, new_cursor_pos)
	N10X.Editor.ExecuteCommand("Delete")