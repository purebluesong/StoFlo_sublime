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
fuctions = ['Save', 'Load', 'Help']

def insert_2_gamefile(msg, mode=':'):
	f = sublime.active_window().open_file('my_story'+story_file_suffix)
	edit = f.begin_edit()
	f.insert(edit, -1, mode + msg)
	f.end_edit(edit)


#working on it , i am trying to make it could handle save and load
def input_handle(num):
	global choose
	if 
		save()
		show_tips_info('Save succeed!')
	elif value in ['L', 'l']:
		chapter = load()
		show_chapter(engine.getChapterContent(chapter))
		show_options(engine.getNextChapters(chapter))
	elif value in ['help', 'H', 'h']:
		show_tips_info('Save succeed!')
	else:
		choose = num



def show_options(options):
	sublime.active_window().show_quick_panel(options+fuctions, input_handle)

def get_choose():
	global choose
	return choose

def save():
	engine.save()

def load():
	saves = engine.get_saves()
	options = []
	for save in saves:
		options += [str(save[0])+'\t' + save[1] + '\t' + save[2]]
	show_options(options)
	i = get_choose()
	return engine.load(i-1)

def choose_story(storys):
	show_options(storys)
	story_index = get_choose()
	if not story_index:	return
	return engine.chooseStory(storys[story_index-1])

def choose_chapter(chapters):
	show_options(chapters)
	return get_choose()

def visit_story(story):
	chapter = startFlag
	engine.resetCurrentChapter()
	while(chapter is not endFlag):# loop the story line
		show_chapter(engine.getChapterContent(chapter))
		show_options(engine.getNextChapters(chapter))
		choose = get_choose()
		while not choose:
			choose = get_choose()
		chapter = engine.chooseChapter(choose-1)
	show_chapter(engine.getChapterContent(endFlag))

def show_chapter(chapter):
	insert_2_gamefile(chapter, ' ')

def show_tips_info(info):
	insert_2_gamefile(info, '> ')

storys = engine.getStoryList()
class StartGameCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global storys
		story = True
		show_tips_info('start game: input \'help\' get help infomation')
		while story:
			story = choose_story(storys)
			if not story:
				break
			visit_story(story)
