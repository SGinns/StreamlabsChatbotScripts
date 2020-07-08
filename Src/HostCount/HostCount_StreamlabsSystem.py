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
import json

#Script Information
ScriptName = "Host Count"
Website = "Coming soon!"
Description = "The count of all the channels hosting you."
Creator = "Rush (Steven Ginns)"
Version = "0.2"

#Variables
configFile = "config.json"
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
lastSave = time.time()

class Settings(object):
	# """ Load in saved settings file if available else set default values. """
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.user = ""
			self.target = 69420
			self.enable_target = True

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
	return


def write_to_file(message):
	if type(message) == str:
		f = open("Services/Scripts/HostCount/AmountOfHosts.txt", "w")
		f.write(message)
		f.close()
		return
	else:
		Parent.log(ScriptName, "message is not of type string is actually {}".format(type(message)))


def getHostCount(api_link):
	if type(api_link) == str:
		global ScriptSettings
		#Get Request
		headers = {
			'Authorization': 'Bearer FDF7u89fdC998875c8d7f'
		}

		return Parent.GetRequest(api_link, headers)
	else:
		Parent.log(ScriptName, "api_link is not a string {}".format(type(api_link)))


def updateHosts():
	global ScriptSettings
	api_link = "https://t.3v.fi/hosts/?ch={}".format(ScriptSettings.user)

	apiResult = getHostCount(api_link)

	data = json.loads(apiResult)

	response = data["response"]

	cutOffIndex = response.find(":")

	if ScriptSettings.enable_target is True:
		outputMessage = "{} / {} Hosts".format(response[:cutOffIndex-6], ScriptSettings.target)
		write_to_file(outputMessage)

		return
	elif ScriptSettings.enable_target is False:
		outputMessage = '{} Hosts'.format(response[:cutOffIndex-6])
		write_to_file(outputMessage)

		return

def Tick():
	global lastSave
	if time.time() - lastSave > 30:
		updateHosts()
		lastSave = time.time()
	return

def SetDefaults():
	global ScriptSettings
	ScriptSettings = Settings()
	ScriptSettings.Save(SettingsFile)
	return