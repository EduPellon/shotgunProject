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
shotgunInfo = validateIDShotgun(goodID)
filters = [['entity','is', {'id': goodID, 'type': inputType}]]
fields = ['id', 'code']
requestVersions= sg.find("Version", filters, fields)
print "Versions in %s:\n" %inputType
for version in requestVersions:
	print version['code']
inputCode = raw_input("Set the name of the new Asset:\n")
final_name = inputCode + ' v001'
for version in requestVersions:
	versionName = version["code"]
	if inputCode.lower() in versionName.lower():
		final_name = "%s%03d" %(versionName[:len(versionName)-3], int(versionName[len(versionName)-3:])+1)
print "El nombre de tu archivo es: %s" %final_name
description = raw_input("Escribe una descripcion de tu version:\n")
data = {
	'code': final_name,
	'entity': {'id': goodID, 'type':inputType},
	'description': description,
	'sg_task': {'id': 2252 , 'type':'Task'},
	'user': {'id':88, 'type': 'HumanUser'},
	'sg_status_list': 'rev',
	'project': {'id':110, 'type':'Project'}
}
result = sg.create("Version", data)
correctPath = False
while correctPath == False:
	file_path = raw_input("Set the file path (include extension):\n")
	if os.path.isfile(file_path) :
		sg.upload("Version", result['id'], file_path, field_name="sg_uploaded_movie", display_name="Media")
		correctPath = True
print "All done, enjoy!"
time.sleep(5)