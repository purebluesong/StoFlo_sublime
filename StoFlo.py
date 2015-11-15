#coding:utf-8
import sublime, sublime_plugin
import engine, stools
# 一个插件150行……我是人民的罪人

helpinfo = u'''帮助信息：
输入S保存进度
输入L载入进度
'''
endFlag = 'end'
startFlag = 'start'
story_file_suffix = '.sfs'
functions = {}
all_options_num = 0
current_story = ''
current_chapter = ''

storys = engine.getStoryList()

prefix_dict = {
	' ': '',
	':': '-',
	'>': '>',
	}

def insert_2_gamefile(msg, mode=':'):
	f = sublime.active_window().open_file('my_story'+story_file_suffix)
	content = ''
	for line in msg.split('\n'):
		content += str(prefix_dict.get(mode)) + line + '\n'
	print content
	edit = f.begin_edit()
	if f.size() == 0:
		f.insert(edit, 0, engine.initmsg+'\n'*5)
	f.insert(edit, f.size(), content)
	f.end_edit(edit)
	f.show_at_center(f.size())

def show_chapter(chapter):
	insert_2_gamefile(chapter, ' ')

def show_tips_info(info):
	insert_2_gamefile(info, '> ')

def show_options(options, function, switch=True):
	global all_options_num
	all_options_num = len(options + functions.keys())
	sublime.active_window().show_quick_panel(options+functions.keys() if switch else options, function)


def save():
	engine.save()
	show_tips_info('Save succeed!')
	return 0

functions['save'] = save

def load_E(choose):
	global current_chapter
	current_chapter = engine.load(choose)
	show_chapter(engine.getChapterContent(current_chapter))
	show_options(engine.getNextChapters(current_chapter), visit_chapter_E)

def load():
	global current_chapter
	saves = engine.get_saves()
	options = []
	for save in saves:
		options += [str(save[0])+'\t' + save[1] + '\t' + save[2]]
	show_options(options, load_E, False)
	return -1

functions['load'] = load

def help():
	show_tips_info(helpinfo)
	return 0

functions['help'] = help

def exit_game():
	exit(0)
	
functions['exit'] = exit_game


def input_handle(num):
	print num
	func_point = all_options_num-num
	print all_options_num, func_point
	functions_num = len(functions)
	if func_point < functions_num:
		choose = functions[functions.keys(functions_num - func_point + 1)]()
	else:
		choose = num+1
	print 'choose' + str(choose)
	return choose

def choose_story_E(num):
	global current_story, current_chapter
	num = input_handle(num)
	if num > 0:
		print 'num' + str(num)
		current_story = storys[num-1]
		engine.chooseStory(current_story)
		print current_story + 'start'
		visit_story(current_story)
	elif num == 0:
		show_options(storys, choose_story_E)

def visit_chapter_E(num):
	global current_chapter
	num = input_handle(num)
	if num > 0:
		chapter = engine.chooseChapter(num-1)
		visit_chapter(current_chapter)
	
def visit_chapter(chapter):
	global endFlag
	print 'visit_chapter:'+chapter
	show_chapter(engine.getChapterContent(chapter))
	if chapter is not endFlag:
		show_options(engine.getNextChapters(chapter), visit_chapter_E)
 
def visit_story(story):
	global startFlag
	engine.resetCurrentChapter()
	visit_chapter(startFlag)

def startGame():
	global storys, current_story, current_chapter
	if current_story:
		if current_chapter:
			visit_chapter(current_chapter)
		else:
			visit_story(current_story)
	else:
		show_tips_info('start game: input \'help\' get help infomation')
		show_options(storys, choose_story_E)	

class StartStoFloGameCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		startGame()
		