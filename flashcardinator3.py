import os
from random import choices
from simple_term_menu import TerminalMenu
from json.decoder import JSONDecodeError
import json

#this is the global vairable assigned when user chooses which topic they would like to study in study()
g_study_topic = ""

#this is the global list where all randomly selected question numbers go. Used by weight_calc() and study()
g_weighted_question_list = []

#this is the list where modifications are made to the questions and then written back to the .study file. Used by study() and weight_calc()
g_editable_questions_list = []


def welcome_menu():
	clear_screen()
	quitting = False
	options = ["Study", "New Flashcard Set", "Add Questions to Existing Cardset", "Quit"]
	mainmenu = TerminalMenu(options)
	while quitting == False:
		print("\nSelect which mode you would like to run\n")
		optionsindex = mainmenu.show()
		optionschoice = options[optionsindex]
		if optionschoice == "Quit":
			quitting = True
		elif optionschoice == "Study":
			study()
		elif optionschoice == "New Flashcard Set":
			new_set()
		elif optionschoice == "Add Questions to Existing Cardset":
			add_questions()


def add_questions():
	print("\nHere are the topics available:\n")
	study_files = os.listdir("./")
	for studyfile in study_files:
		if ".study" in studyfile:
			print('\t' + "-" + studyfile.replace('.study', ''))
	topic_answer = input("\nWhich Topic would you like to add questions to?\n")
	more_questions = ""
	question_dict = []
	already_used_ids_in_set = [0]
	next_id = 0
	with open(topic_answer + '.study') as file:
		try:
			data = json.load(file)
			for i in data:
				already_used_ids_in_set = i.get("id")
			if already_used_ids_in_set != 0:
				next_id = already_used_ids_in_set + 1
		except JSONDecodeError:
			pass
	try:
		question_dict = data
	except:
		pass
	while more_questions == "":
		user_question = input("Please Type Your Question Below, Press Enter when finished:\n")
		user_answer = input("Please Type The Answer to Your Question Below, Press Enter when finished:\n")
		new_question = {"id":next_id,"question":user_question,"answer":user_answer,"weight":100,"asked":"false"}
		question_dict.append(new_question)
		next_id += 1
		answer = input("Do you have more questions to add? (Y/n)\n")
		if answer == "Y" or answer == "y":
			more_questions = ""
		if answer == "N" or answer == "n":
			with open(topic_answer + ".study", "w") as file:
				json.dump(question_dict, file)
			more_questions = "nomore"


def new_set():
	set_name = input("What Topic Will This Flashcard Set Cover?\n")
	set_name = set_name + ".study"
	f = open(set_name, "a")
	f.close()	
	add_qs = input("New Flashcard Set Created. Would you like to add questions now? (y/N)\n")
	if add_qs == "Y" or add_qs == "y":
		add_questions()
	elif add_qs == "N" or add_qs == "n":
		print("Okay, see you later.")



def study():
	global g_study_topic
	global g_weighted_question_list
#starting user interaction portion
	study_files = os.listdir("./")
	for studyfile in study_files:
		if ".study" in studyfile:
			print('\t' + "-" + studyfile.replace('.study', ''))
	study_topic_answer = input("\nWhich topic would you like to study?\n")
	g_study_topic = study_topic_answer + ".study"
	was_studying_earlier = input("\nWould you like to pick up where you left off? (y/N): ")
	if was_studying_earlier == 'y' or was_studying_earlier == 'Y':
		weight_calc(True)
	else:
		weight_calc(False)
	
	for i in g_weighted_question_list:
		clear_screen()
		print("Question: " + g_editable_questions_list[i]['question'])
		input("Press Enter to see answer\n")
		print("Answer: " + g_editable_questions_list[i]['answer'])
		correct = input("\nDid you get the question correct? (Y/N): ")
		if correct == 'y' or correct == 'Y':
			g_editable_questions_list[i]['weight'] = g_editable_questions_list[i]['weight'] - 10
			g_editable_questions_list[i]['asked'] = "true"
		elif correct == 'n' or correct == 'N':
			g_editable_questions_list[i]['weight'] = g_editable_questions_list[i]['weight'] + 10
			g_editable_questions_list[i]['asked'] = "true"

	with open(study_topic_answer + ".study", "w") as file:
		json.dump(g_editable_questions_list, file)


def weight_calc(result_of_study_question):
	global g_study_topic
	global g_weighted_question_list
	global g_editable_questions_list
	weights = []
	list_of_ids = []
	editable_questions_list = []
	
	with open(g_study_topic) as file:
		data = json.load(file)
		for i in data:
			editable_questions_list.append(i)

	g_editable_questions_list = editable_questions_list

	if result_of_study_question == False:
		for i in editable_questions_list:
			if i["asked"] == "true":
				i["asked"] = "false"
		for i in editable_questions_list:
			weights.append(i["weight"])
			list_of_ids.append(i['id'])
		random_question_numbers = choices(list_of_ids, weights = weights, k=25)
		g_weighted_question_list = list(dict.fromkeys(random_question_numbers))

	elif result_of_study_question == True:
		for i in editable_questions_list:
			if i["asked"] == "false":
				weights.append(i["weight"])
				list_of_ids.append(i['id'])
		random_question_numbers = choices(list_of_ids, weights = weights, k=25)
		g_weighted_question_list = list(dict.fromkeys(random_question_numbers))

def clear_screen():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')


welcome_menu()



