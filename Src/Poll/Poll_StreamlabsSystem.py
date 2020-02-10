#Imports
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

import sys
import json
import os
import ctypes
import codecs
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "Entities"))
import Question
from Vote import Vote

#Script Information
ScriptName = "Poll"
Website = "Coming soon!"
Description = ""
Creator = "Rush (Steven Ginns)"
Version = "0.1"

#Variables
configFile = "config.json"
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
fullQuestion = Question

class Settings(object):
	# """ Load in saved settings file if available else set default values. """
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.liveOnly = False
			self.command = "!poll"
			self.channelStreamer = ""
			self.questionTimer = 30

	def Reload(self, jsondata):
		# """ Reload settings from AnkhBot user interface by given json data. """
		self.__dict__ = json.loads(jsondata, encoding="utf-8")
		return

	def Save(self, settingsfile):
		# """ Save settings contained within to .json and .js settings files. """
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
				json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
			with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
				f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
		except:
			Parent.Log(ScriptName, "Failed to save settings to file.")
		return

#Initialise data on load
def Init():
	global ScriptSettings
	ScriptSettings = Settings(SettingsFile)
	return

#Reload settings on save
def ReloadSettings(jsondata):
	global ScriptSettings
	ScriptSettings.Reload(jsondata)
	return

#Save settings as the script is unloaded
def Unload():
	ScriptSettings.Save(SettingsFile)
	return

def ScriptToggled(state):
	global ScriptSettings
	if not state:
		ScriptSettings.Save(SettingsFile)
	return

def Execute(data):
	global ScriptSettings
	global fullQuestion

	if data.IsChatMessage() and data.IsFromTwitch() and data.GetParam(0).lower() == ScriptSettings.command and ScriptSettings.channelStreamer.lower() == data.User:
		questionId = ''

		if data.GetParamCount() > 2:
			for i in range(1, data.GetParamCount()):
				questionId += "{}_".format(data.GetParam(i))

			questionId = questionId[:-1]
		else:
			questionId = data.GetParam(1)

		fullQuestion = Question.ReadQuestion(questionId, ScriptSettings.questionTimer)

		if type(fullQuestion) == str and fullQuestion.startswith("[Warning"): #Question warnings
			Parent.SendStreamMessage(fullQuestion)
			return
		elif type(fullQuestion) == list:
			options = "["
			for option in fullQuestion[1]:
				options += option+", "

			for option in fullQuestion[1]:
				Vote.resultDict.update({option: 0})
			
			Parent.SendStreamMessage(fullQuestion[0]+"Please vote with an option "+options[:-2]+"]")

			Vote.canVote = True
			Vote.timeOpened = time.time()
		elif fullQuestion.startswith("[Issue"):
			Parent.SendStreamMessage(fullQuestion[0])
			Parent.Log(ScriptName, "Method: ReadQuestion. Question Type and/or timer are not the correct types.")
			Parent.SendStreamMessage(fullQuestion)
			return
		else:
			Parent.Log(ScriptName, "Did not return the string warning of configuration list")
			Parent.SendStreamMessage("[Warning - Issue logged {Scripts -> (i)} ] Send the log to Steven#0097 on Discord.")
			return
	elif data.IsChatMessage() and data.IsFromTwitch() and data.Message in fullQuestion[1] and Parent.IsOnUserCooldown(ScriptName, data.Message, data.User) == False and Vote.canVote == True:
		Vote.resultDict[data.Message] += 1
		for option in fullQuestion[1]:
			Parent.AddUserCooldown(ScriptName, option, data.User, ScriptSettings.questionTimer+5)
		return

def Tick():
	if Vote.canVote == True and time.time() - Vote.timeOpened >= ScriptSettings.questionTimer:
		Vote.canVote = False
		displayResults()

def displayResults():
	itemMaxValue = max(Vote.resultDict.items(), key=lambda x: x[1])
	victoriousOptions = []

	for key, value in Vote.resultDict.items():
		if value == itemMaxValue[1]:
			victoriousOptions.append(key)

	winningOptions = "["
	for option in victoriousOptions:
		winningOptions += option+", "

	Parent.SendStreamMessage("The results are in and the winning option(s) are "+winningOptions[:-2]+"] with "+str(itemMaxValue[1])+" vote(s)!")

	Vote.resultDict = {}

def SetDefaults():
	global ScriptSettings
	ScriptSettings = Settings()
	ScriptSettings.Save(SettingsFile)
	return
