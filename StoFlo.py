#coding:utf-8
import sublime, sublime_plugin
import engine, stools
helpinfo = u'''帮助信息：
输入S保存进度
输入L载入进度
'''
endFlag = 'end'
startFlag = 'start'
story_file_suffix = '.sfs'
choose = 0
functions = {}
all_options_num = 0
current_story = ''
current_chapter = ''

prefix_dict = {
	' ': '',
	':': '-',
	'>': '>',
	}

def insert_2_gamefile(msg, mode=':'):
	f = sublime.active_window().open_file('my_story'+story_file_suffix)
	content = ''
	for line in msg.split('\n'):
		content += str(prefix_dict.get(mode)) + line
	edit = f.begin_edit()
	f.insert(edit, -1, content)
	f.end_edit(edit)
	f.show_at_center(f.size())

def show_chapter(chapter):
	insert_2_gamefile(chapter, ' ')

def show_tips_info(info):
	insert_2_gamefile(info, '> ')



def show_options(options, function):
	global all_options_num
	all_options_num = len(options + functions.keys())
	sublime.active_window().show_quick_panel(options+functions.keys(), function)

def get_choose():
	global choose
	print 'get_choose' + str(choose)
	return choose

def save():
	engine.save()
	show_tips_info('Save succeed!')

functions['save'] = save

def load():
	saves = engine.get_saves()
	options = []
	for save in saves:
		options += [str(save[0])+'\t' + save[1] + '\t' + save[2]]
	show_options(options)
	i = get_choose()
	chapter = engine.load(i-1)
	show_chapter(engine.getChapterContent(chapter))
	show_options(engine.getNextChapters(chapter))
	return chapter

functions['load'] = load

def help():
	show_tips_info(helpinfo)

functions['help'] = help

def exit_game():
	exit(0)
	
functions['exit'] = exit_game


def input_handle(num):
	global choose
	print num
	func_point = all_options_num-num
	print all_options_num, func_point
	functions_num = len(functions)
	if func_point < functions_num:
		functions[functions.keys(functions_num - func_point + 1)]()
		choose = 0
	else:
		choose = num+1
	print 'set_choose'+str(choose)
	return choose

def choose_story_E(num):
	global current_story
	num = input_handle(num) 
	if not num:
		print 'num' + str(num)
		current_story = storys[num-1]
		engine.chooseStory(current_story)
		print sto + 'start'
		visit_story(current_story)

def choose_chapter(chapters):
	show_options(chapters)
	return get_choose()

def visit_chapter(chapter):
	while(chapter is not endFlag):# loop the story line
		show_chapter(engine.getChapterContent(chapter))
		show_options(engine.getNextChapters(chapter))
		choose = get_choose()
		while not choose:
			choose = get_choose()
		chapter = engine.chooseChapter(choose-1)
	show_chapter(engine.getChapterContent(endFlag))

def visit_story(story):
	engine.resetCurrentChapter()
	visit_chapter(startFlag)


storys = engine.getStoryList()

def startGame():
	global storys, current_story, current_chapter
	if current_story:
		if current_chapter:
			visit_chapter(current_chapter)
		else:
			visit_story(current_story)
	else :
		show_tips_info('start game: input \'help\' get help infomation')
		show_options(storys, choose_story_E)
		


class StartGameCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		startGame()
		