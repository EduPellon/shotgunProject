import os, sys
from shotgun_api3 import Shotgun
import os.path
import time

sg = Shotgun("https://upgdl.shotgunstudio.com", "NachoScript", "486c9aa2bf63e4a83f975e3928207342e15dfcfeb2066384d7e48f9da7087923" )

def validateType(userInputType):
	validationType = False
	while validationType == False:
		if userInputType == 'asset':
			return "Asset"
		elif userInputType == 'shot':
			return "Shot"
		else:
			userInputType = raw_input("ERROR, Invalid data. Try again\nWhat do you want to upload?\n->Asset\n->Shot\n").lower()

def validateID(userInputID):
	validationNumber = False
	while validationNumber == False:
		try:
			userInputID = int(userInputID)
			return userInputID
		except:
			userInputID = raw_input("ERROR! The ID must be a number\n")
def validateIDShotgun(validatedID):
	shotgunValidation = False
	while shotgunValidation == False:
		shotgunFile = sg.find_one(inputType, [["id", "is", validatedID]], ["id", "code", "sg_status_list"])
		if shotgunFile == None:
			newID = raw_input("No %s founded in the project, try another ID:\n" %inputType)
			try:
				validatedID = validateID(newID)
			except Exception as e:
				print e
		else:
			print "The %s found name is: %s \n" %(inputType, shotgunFile['code'])
			return shotgunFile





option = raw_input("What do you want to upload?\n->Asset\n->Shot\n").lower()
inputType = validateType(option)
ID = raw_input("Type the ID of the %s:" %inputType) 
goodID = validateID(ID)
print validateIDShotgun(goodID)
shotgunInfo = validateIDShotgun(goodID)

print "Data correct"
time.sleep(5)