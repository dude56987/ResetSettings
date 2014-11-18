#! /usr/bin/python
########################################################################
# Resets settings to defaults from /etc/skel.
# Copyright (C) 2013  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
# thunar custom actions are stored in ~/.config/Thunar/uca.xml
# copy a premade version of that file to each users directory
import shutil
import os
import sys
########################################################################
# TODO:
#  * Add lock settings option which requires root, this will chown the 
#    owner of the config files to root so the user cant change the 
#    settings.
#  * Make the -u user command and -p preset command work together to 
#    edit the specific user specified preset settings
#    - Later on this should also work with the above lock setting
#  * Make a command that will backup all current user settings to the 
#    /etc/skel directory 
########################################################################
def makeDir(remoteDir):
	import os
	''' Creates the defined directory, if a list of directorys are listed
	that do not exist then they will be created aswell, so beware of 
	spelling mistakes as this will create the specified directory you 
	type mindlessly.'''
	temp = remoteDir.split('/')
	remoteDir= ''
	for i in temp:
		remoteDir += (i + '/')
		if os.path.exists(remoteDir):
			print remoteDir , ': Already exists!, Moving on...'
		else:
			os.mkdir(remoteDir)
########################################################################
def loadFile(fileName):
	try:
		sys.stdout.write(("Loading :"+fileName))
		fileObject=open(fileName,'r');
	except:
		print "Failed to load :",fileName
		return False
	fileText=''
	lineCount = 0
	for line in fileObject:
		if line[:1] != '#':
			fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount += 1
	sys.stdout.write(("Finished Loading :"+fileName+'\r'))
	sys.stdout.write(('                                                   \r'))
	fileObject.close()
	if fileText == None:
		return False
	else:
		return fileText
	#if somehow everything fails return false
	return False
########################################################################
def writeFile(fileName,contentToWrite):
	# figure out the file path
	filepath = fileName.split(os.sep)
	filepath.pop()
	filepath = os.sep.join(filepath)
	# check if path exists
	if os.path.exists(filepath):
		try:
			fileObject = open(fileName,'w')
			fileObject.write(contentToWrite)
			fileObject.close()
			print 'Wrote file:',fileName
		except:
			print 'Failed to write file:',fileName
			return False
	else:
		print 'Failed to write file, path:',filepath,'does not exist!'
		return False
########################################################################
def currentDirectory():
	currentDirectory = os.path.abspath(__file__)
	temp = currentDirectory.split(os.path.sep)
	currentDirectory = ''
	for item in range((len(temp)-1)):
		if len(temp[item]) != 0:
			currentDirectory += os.path.sep+temp[item]
	return (currentDirectory+os.path.sep)
########################################################################
#Function that opens a xml file and reads data from a set of tags
def xmlTagValues(fileName,tagValue):
	'''Open a file (fileName) and search line by line through the 
	file for every occurrence of a xml tag (tagValue) and return the 
	values inside each of the tags in an array. If no values are 
	found the function will return the value (None). NOTE: This can 
	not find multiples of the same tag if they are on the same 
	line.'''
	from re import sub,search,findall
	#open the specified file
	fileObject = open(fileName,'r')
	# create local variables to be used latter
	temp = ''
	totalTags = 0
	values = []
	# loop through the lines in the file
	for i in fileObject:
		if i[:1] != '#':
			# remove all newlines and tabs
			i = sub('\n','',i)
			i = sub('\t+','',i)
			temp += i
			if search(('<'+tagValue+'>'),i) != None:
				totalTags += 1
	# close the file to save memory
	fileObject.close()
	# if the tag specified by the user was not found in the file return
	# None
	if totalTags == 0:
		return None
	else:
		# Loop through the string as many times as the tag is found
		for x in range(len(findall(('<'+tagValue+'>'),temp))):
			# Find the front and back of the value inside the tags to cut it out
			front = (temp.find(('<'+tagValue+'>'))+len(('<'+tagValue+'>')))
			back = temp.find(('</'+tagValue+'>'))
			# add the values into the (values) array
			values.append(temp[front:back])
			# cut the temp string up to the end of the last string worked on
			temp = temp[(back+len(tagValue+'>')):]
		return values
########################################################################
def grabXmlValues(inputString, tagValue):
	'''Gets all xml values from a text string matching the search value
	and returns an array'''
	from re import sub,search,findall
	tagValue = str(tagValue)# just in case
	totalTags = inputString.find(tagValue)
	values = []
	temp = inputString
	if totalTags == -1:
		#~ print 'XML values do not exist for '+tagValue
		return []
	else:
		# Loop through the string as many times as the tag is found
		#~ while temp.find(('<'+tagValue+'>')):
		for x in range(len(findall(('<'+tagValue+'>'),temp))):
			# Find the front and back of the value inside the tags to cut it out
			front = (temp.find(('<'+tagValue+'>'))+len(('<'+tagValue+'>')))
			back = temp.find(('</'+tagValue+'>'))
			# add the values into the (values) array
			values.append(temp[front:back])
			#~ print 'CUT','front',front,'back',back,'lenth',len(temp) # DEBUG
			#~ print temp[front:back]
			# cut the temp string up to the end of the last string worked on
			temp = temp[(back+len(tagValue+'>')):]
		return values
########################################################################
def resetSettings(username):
	# build the themes/icons/fonts folder
	makeDir(str(os.path.join('/home',username,'.icons')))
	makeDir(str(os.path.join('/home',username,'.themes')))
	makeDir(str(os.path.join('/home',username,'.fonts')))
	# copy over /etc/skel recursively
	os.system(('sudo cp -rvf /etc/skel/. '+os.path.join('/home',username)))
	#~ shutil.copytree('/etc/skel',os.path.join('/home',username))
	# set user ownership for local files
	print ('sudo chown --recursive '+username+' '+os.path.join('/home',username))
	os.system('sudo chown --recursive '+username+' '+os.path.join('/home',username))
	# warn user to logout and back in to refresh settings
	print 'It is recomended that you logout and back in to refresh your settings!'
	print 'If you dont you may notice some issues...'
########################################################################
def getSettings():
	# try to load the config file locally first
	if os.path.exists('resetsettings.xml'):
		dataValues = loadFile('resetsettings.xml')
	else:
		# load config file does not exist locally load the one in etc from installed version
		dataValues = loadFile('/etc/resetsettings.xml')
	if dataValues == False:
		print 'ERROR: No config files have been created!'
		return False
	# rip file into an array of values based on the <preset> tag
	dataValues = grabXmlValues(dataValues,'preset')
	# create data to store array 
	data = []
	for preset in dataValues:
		# presets xml are striped into a dict
		data.append({'name':(grabXmlValues(preset,'name')),'file':(grabXmlValues(preset,'file')),'folder':(grabXmlValues(preset,'folder')),'command':(grabXmlValues(preset,'command'))})
	# return an array of dicts
	return data
########################################################################
# globals
userName = os.popen('whoami').readline().split('\n')[0]
# MAIN PROGRAM
defaultRun = True; # used for when system arguments are not used
# split the arguments by - signs to pull arguments more correctly
# this allows you to split that result by spaces for arguments with multuple entries
inputs = ' '.join(sys.argv).replace('--','-').split('-')
for arg in inputs:
	argument = arg.split(' ')
	mainArgument = argument[0]
	if (mainArgument in ['h','help']):
		defaultRun = False
		print "Resets settings to defaults from /etc/skel."
		print "Copyright (C) 2013  Carl J Smith"
		print ""
		print "This program is free software: you can redistribute it and/or modify"
		print "it under the terms of the GNU General Public License as published by"
		print "the Free Software Foundation, either version 3 of the License, or"
		print "(at your option) any later version."
		print ""
		print "This program is distributed in the hope that it will be useful,"
		print "but WITHOUT ANY WARRANTY; without even the implied warranty of"
		print "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
		print "GNU General Public License for more details."
		print ""
		print "You should have received a copy of the GNU General Public License"
		print "along with this program.  If not, see <http://www.gnu.org/licenses/>."
		print "#############################################################"
		print "-h or --help"
		print "    Displays this menu"
		print "-u or --user"
		print "    Resets the settings for the specified user to the system defaults"
		print '    Multuple users can be used. e.g. resetsetting -u bob john ted'
		print '-l or --list'
		print '    Lists the presets defined in the preset config file. The'
		print '    config file is stored in /etc/resetsettings.xml'
		print '-p or --preset'
		print '    Resets only the preset program to defaults in /etc/skel'
		print '-b or --backup'
		print '    This will create a backup based on a preset. The backup will be'
		print '    stored at the location defined in the preset, appended with '
		print '    .backup. So config.xml will become config.xml.backup. This file'
		print '    will be stored in the same location as the orignal file.'
		print '-r or --restore'
		print '    Restore settings from a backup created with the --backup'
		print '    command defined above. If a backup has not been created'
		print '    nothing will happen. This and the above command will only'
		print '    work with presets defined in the config file.'
		print '#############################################################'
	elif (mainArgument in ['u','user']):
		defaultRun = False
		#check for root since shortcuts need to be installed for all users
		if os.geteuid() != 0:
			print 'ERROR: this argument must be ran as root!'
			print 'This parameter reset settings for a specified user!'
			exit()
		else:
			for item in argument: 
				# compare the username given with users home folders
				if os.path.exists(os.path.join('/home',item)):
					# reset the users settings for the perfered user
					resetSettings(item)
	elif (mainArgument in ['l','list']):
		defaultRun = False
		# This command will list all presets
		data = getSettings()
		print 'The following presets are stored in /etc/resetsettings.xml'
		print ('='*20)
		for index in data:
			for name in index['name']:
				print ('* "'+name+'"')
		print
		print ('='*20)
		print 'To use a reset preset type "resetsettings -p presetName"'
		print ('='*20)
		print 'To search these presets use "resetsettings -l | grep appname"'
		print ('='*20)
	elif (mainArgument in ['p','preset']):
		defaultRun = False
		userName = os.popen('whoami').readline().split('\n')[0]
		# for running a preset this will reset specific user settings based on the presets config file
		data = getSettings()
		for index in data:
			for name in index['name']:
				if (name in sys.argv):
					print ('Reseting the settings for '+name+'...')
					for filename in index['file']:
						print ('cp -vf /etc/skel/'+filename+' /home/'+userName+'/'+filename)
						os.system('cp -vf /etc/skel/'+filename+' /home/'+userName+'/'+filename)
					for folder in index['folder']:
						print ('cp -vrf /etc/skel/'+folder+' /home/'+userName+'/'+folder)
						os.system('cp -vrf /etc/skel/'+folder+' /home/'+userName+'/'+folder)
					for command in index['command']:
						print command
						os.system(command)
	elif (mainArgument in ['b','backup']):
		defaultRun = False
		userName = os.popen('whoami').readline().split('\n')[0]
		# for running a preset this will backup specific user settings based on the presets config file
		data = getSettings()
		for index in data:
			for name in index['name']:
				if (name in sys.argv):
					print ('Creating a backup of the settings for '+name+'...')
					for filename in index['file']:
						print ('cp -vf /home/'+userName+'/'+filename+' /home/'+userName+'/.backups/'+filename)
						os.system('cp -vf /home/'+userName+'/'+filename+' /home/'+userName+'/.backups/'+filename)
					for folder in index['folder']:
						print ('mkdir -p /home/'+userName+'/.backups/'+folder)
						os.system('mkdir -p /home/'+userName+'/.backups/'+folder)
						print ('cp -vrf /home/'+userName+'/'+folder+'. /home/'+userName+'/.backups/'+folder)
						os.system('cp -vrf /home/'+userName+'/'+folder+'. /home/'+userName+'/.backups/'+folder)
	elif (mainArgument in ['r','restore']):
		defaultRun = False
		userName = os.popen('whoami').readline().split('\n')[0]
		# for running a preset this will restore specific user settings based on the presets config file that have been backed up with the backup command
		data = getSettings()
		for index in data:
			for name in index['name']:
				if (name in sys.argv):
					print ('Restoring the settings for '+name+'...')
					for filename in index['file']:
						print ('cp -vf /home/'+userName+'/.backups/'+filename+' /home/'+userName+'/'+filename)
						os.system('cp -vf /home/'+userName+'/.backups/'+filename+' /home/'+userName+'/'+filename)
					for folder in index['folder']:
						print ('cp -vrf /home/'+userName+'/.backups/'+folder[:len(folder)-1]+'/. /home/'+userName+'/'+folder)
						os.system('cp -vrf /home/'+userName+'/.backups/'+folder[:len(folder)-1]+'/. /home/'+userName+'/'+folder)
if defaultRun == True: # by default run the program for the current user but confirm operation
	if ((('-f' in sys.argv)) or (('--force' in sys.argv))):
		# force the program on without confirmation
		userName = os.popen('whoami').readline().split('\n')[0]
		resetSettings(userName)
	else:
		# warn user and check before overwriting settings
		print '################################################################################'
		print 'WARNING THIS PROGRAM WILL RESET THE USER SETTINGS TO THE SYSTEM DEFAULT!!!'
		print '################################################################################'
		print ' * This program will reset user settings, changing things back to thier default!'
		print ' * This will not remove any software from your computer!'
		print ' * May change settings you dont want it to!'
		print 'Are you sure you would like to reset YOUR user settings???'
		query = raw_input('[y/n]: ')
		if query == 'y':
			userName = os.popen('whoami').readline().split('\n')[0]
			resetSettings(userName)
			print '#####################################################'
			print 'PLEASE REBOOT THE SYSTEM TO FINALIZE THE RESET!'
			print '#####################################################'
			print 'NOTE: You may be able to logout and back in to reset'
			print '      the changes, although it is still recomended'
			print '      to do a full reboot.'
			print '#####################################################'

exit()
