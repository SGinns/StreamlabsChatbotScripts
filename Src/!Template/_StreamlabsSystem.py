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

#Script Information
ScriptName = ""
Website = "Coming soon!"
Description = ""
Creator = "Rush (Steven Ginns)"
Version = "0.1"

#Variables
configFile = "config.json"
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

class Settings(object):
	# """ Load in saved settings file if available else set default values. """
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.liveOnly = False
			self.command = "!"
			self.permission = "Everyone"
			self.cooldown = 0
			self.onCooldown = "$user, $command is still on cooldown for $time!"
			self.userCooldown = 0
			self.onUserCooldown = "$user, you are still on cooldown for $time!"

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

	if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.command and ((ScriptSettings.liveOnly and Parent.IsLive() or (not ScriptSettings.liveOnly))):
	return

def Tick():
	return

def SetDefaults():
	global ScriptSettings
	ScriptSettings = Settings()
	ScriptSettings.Save(SettingsFile)
	return