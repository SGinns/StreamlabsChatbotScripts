import clr
import sys
import json
import os
import ctypes
import codecs
import re

ScriptName = "Nom"
Website = "Coming soon!"
Description = "Nom upon your star power!"
Creator = "Rush (Steven Ginns)"
Version = "0.1.4"

configFile = "config.json"
settings = {}

def ScriptToggled(state):
	return

def Init():
	global settings

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": False,
			"command": "!nom",
			"permission": "Everyone",
			"useCustomCosts": True,
			"costs": 0,
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 3,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 300,
			"onUserCooldown": "$user $command is still on user cooldown for $cd minutes!",
			"responseInvalidInput": "$user please enter a positive number with no decimal places",
			"responseNotEnoughPoints": "$user you do not have enough $currency, sit back, relax and watch the stream to get some $currency <3",
			"responseSpecifyMorePoints": "$user are you not hungry? Try eating more $currency :)",
			"responseMultipleSuccessful": "$user just devoured $number large $currency",
			"responseSingularSuccessful": "$user just devoured 1 large $currency"
		}

def isPlural(currency):
	if "ss" in currency[-2:]:
		return False
	elif "ies" in currency[-3:]:
		return True
	elif "es" in currency[-2:]:
		return True
	elif "s" in currency[-1:]:
		return True
	else:
		return False

def updateToUnpluralisedlName(currency):
	if "ss" in currency[-2:]:
		return currency
	elif isPlural(currency) == True and "ies" in currency[-3:]:
		currency = currency[:len(currency)-3] + 'y'
		return currency
	elif isPlural(currency) == True and "es" in currency[-2:]:
		currency = currency[:len(currency)-2]
		return currency
	elif isPlural(currency) == True and "s" in currency[-1:]:
		currency = currency[:len(currency)-1]
		return currency

def updateToPluralName(currency):
	if isPlural(currency) == False and ("ch" in currency[-2:] or "sh" in currency[-2:]):
		currency += "es"
		return currency
	if isPlural(currency) == False and ("s" in currency[-1:] or "x" in currency[-1:] or "z" in currency[-1:]):
		currency += "es"
		return currency
	if isPlural(currency) == False and ("oy" in currency[-2:] or "ey" in currency[-2:]):
		currency += "s"
		return currency
	elif isPlural(currency) == False and "y" in currency[-1:]:
		currency = currency[:len(currency)-1]
		currency += "ies"
		return currency
	else:
		currency += "s"
		return currency

#--- This is when the currency name is actually "s" or "ies" ---#
def isTheNameAPluralEnding(currency):
	if currency == "s" or currency == "ies" or currency == "es":
		return True
	else:
		return False

def Execute(data):
	userId = data.User
	username = data.UserName
	userPointCount = Parent.GetPoints(userId)
	pointsToSpend = data.GetParam(1)
	currency = Parent.GetCurrencyName()
	outputMessage = ""

	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		if data.GetParamCount() == 1:
			if userPointCount >= 1 and userPointCount >= settings["costs"]:
				Parent.RemovePoints(userId, username, 1)

				outputMessage = settings["responseSingularSuccessful"]
				outputMessage = outputMessage.replace("$user", username)

				if isTheNameAPluralEnding(currency) == True:
					pass
				elif isPlural(currency):
					currency = updateToUnpluralisedlName(currency)

				outputMessage = outputMessage.replace("$currency", currency)
				
				Parent.SendStreamMessage(outputMessage)
				return
			else:
				outputMessage = settings["responseNotEnoughPoints"]
				outputMessage = outputMessage.replace("$user", username)
				outputMessage = outputMessage.replace("$currency", currency)
				
				Parent.SendStreamMessage(outputMessage)
				return
		elif data.GetParamCount() > 1:
			if (pointsToSpend).isdigit() == False:
				outputMessage = settings["responseInvalidInput"]
				outputMessage = outputMessage.replace("$user", username)

				Parent.SendStreamMessage(outputMessage)
				return
			if int(pointsToSpend) == 0:
				outputMessage = settings["responseSpecifyMorePoints"]
				outputMessage = outputMessage.replace("$user", username)
				outputMessage = outputMessage.replace("$currency", currency)

				Parent.SendStreamMessage(outputMessage)
				return
			if userPointCount == 0 or userPointCount < int(pointsToSpend) or userPointCount < settings["costs"]:
				outputMessage = settings["responseNotEnoughPoints"]
				outputMessage = outputMessage.replace("$user", username)
				outputMessage = outputMessage.replace("$currency", currency)

				Parent.SendStreamMessage(outputMessage)
				return
			if userPointCount >= int(pointsToSpend):
				Parent.RemovePoints(userId, username, int(pointsToSpend))

				outputMessage = settings["responseMultipleSuccessful"]
				outputMessage = outputMessage.replace("$user", username)
				outputMessage = outputMessage.replace("$number", pointsToSpend)
				
				if int(pointsToSpend) == 1:
					if isPlural(currency) == True:
						currency = updateToUnpluralisedlName(currency)
				elif int(pointsToSpend) > 1:
					if isPlural(currency) == False:
						currency = updateToPluralName(currency)

				outputMessage = outputMessage.replace("$currency", currency)
				
				Parent.SendStreamMessage(outputMessage)
				return
			else:
				Parent.SendStreamMessage("Unknown Issue: Please contact Steven#0097 on discord with a screenshot of the command inputted and any output.")
				return
	return

def ReloadSettings(jsonData):
	Init()
	return

def OpenReadMe():
	location = os.path.join(os.path.dirname(__file__), "README.txt")
	os.startfile(location)
	return

def Tick():
	return