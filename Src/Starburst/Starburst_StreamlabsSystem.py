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
from datetime import timedelta
from random import SystemRandom

#Script Information
ScriptName = "Starburst"
Website = "Coming soon!"
Description = "Distribute currency to everyone in the stream!"
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
			self.command = "!starburst"
			self.permission = "VIP Exclusive"
			self.beginStarburst = "justni1King $user has shattered a star source giving out $amount $currency to chat justni1SStar"
			self.onCooldown = "$user, $command is still on cooldown for $time!"
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

def getFormattedDuration(unformattedDuration):
	return str(timedelta(seconds=unformattedDuration))

def Execute(data):
	userId = data.User
	username = data.UserName
	currencyName = Parent.GetCurrencyName()
	outputMessage = ""
	systemRandom = SystemRandom()
	global ScriptSettings

	if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.command and ((ScriptSettings.liveOnly and Parent.IsLive() or (not ScriptSettings.liveOnly))):
		if Parent.HasPermission(data.User, "VIP Exclusive", "") == True:
			if Parent.IsOnCooldown(ScriptName, ScriptSettings.command):
				time = getFormattedDuration(Parent.GetCooldownDuration(ScriptName, ScriptSettings.command))
				outputMessage = ScriptSettings.onCooldown.replace("$user", username).replace("$command", ScriptSettings.command).replace("$time", time)
				return Parent.SendStreamMessage(outputMessage)
			elif Parent.IsOnUserCooldown(ScriptName, ScriptSettings.command, userId):
				time = getFormattedDuration(Parent.GetUserCooldownDuration(ScriptName, ScriptSettings.command, userId))
				outputMessage = ScriptSettings.onUserCooldown.replace("$user", username).replace("$time", time)
				return Parent.SendStreamMessage(outputMessage)
			else:
				amount = systemRandom.randint(10, 40)
				Parent.SendStreamMessage(ScriptSettings.beginStarburst.replace("$user", username).replace("$amount", str(amount)).replace("$currency", currencyName))

				activeViewersList = Parent.GetActiveUsers()

				for viewer in activeViewersList:
					Parent.AddPoints(viewer, Parent.GetDisplayName(viewer), amount)
				
				Parent.AddCooldown(ScriptName, ScriptSettings.command, 100)
				Parent.AddUserCooldown(ScriptName, ScriptSettings.command, userId, 43200)
	return

def Tick():
	return

def SetDefaults():
	global ScriptSettings
	ScriptSettings = Settings()
	ScriptSettings.Save(SettingsFile)
	return