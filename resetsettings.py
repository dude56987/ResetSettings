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
	os.system('sudo chown --recursive '+username+' '+os.path.join('/home',username))
	# warn user to logout and back in to refresh settings
	print 'It is recomended that you logout and back in to refresh your settings!'
	print 'If you dont you may notice some issues...'
########################################################################
def getSettings():
	if os.path.exists('resetsettings.xml'):
		dataValues = loadFile('resetsettings.xml')
	else:
		dataValues = loadFile('/etc/resetsettings.xml')
	if dataValues == False:
		print 'ERROR: No config files have been created!'
		return False
	data = []
	dataValues = grabXmlValues(dataValues,'preset')

	for index in dataValues:
		temp = index
		data.append({'name':(grabXmlValues(temp,'name')),'file':(grabXmlValues(temp,'file')),'folder':(grabXmlValues(temp,'folder')),'command':(grabXmlValues(temp,'command'))})
	return data
########################################################################
# globals
userName = os.popen('whoami').readline().split('\n')[0]
# MAIN PROGRAM
defaultRun = True; # used for when system arguments are not used
inputs = ' '.join(sys.argv).replace('--','-').split('-')
for arg in inputs:
	temp = arg.split(' ')
	if ((('h' == temp[0])) or (('help' == temp[0]))):
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
	elif ((('u' == temp[0])) or (('user' == temp[0]))):
		defaultRun = False
		#check for root since shortcuts need to be installed for all users
		if os.geteuid() != 0:
			print 'ERROR: this argument must be ran as root!'
			print 'This parameter reset settings for a specified user!'
			exit()
		else:
			for item in temp: 
				# compare the username given with users home folders
				if os.path.exists(os.path.join('/home',item)):
					# reset the users settings for the perfered user
					resetSettings(item)
	elif ((('l' == temp[0])) or (('list' == temp[0]))):
		defaultRun = False
		# This command will list all presets
		data = getSettings()
		print 'The following presets have been created...'
		for index in data:
			for name in index['name']:
				print ('* "'+name+'"')
		print
		print 'To use a reset preset type resetsettings -p presetName'
	elif ((('p' == temp[0])) or (('preset' == temp[0]))):
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
		os.system('sudo chown -R '+userName+' '+os.path.join('/home',userName))
	elif ((('b' == temp[0])) or (('backup' == temp[0]))):
		defaultRun = False
		userName = os.popen('whoami').readline().split('\n')[0]
		# for running a preset this will backup specific user settings based on the presets config file
		data = getSettings()
		for index in data:
			for name in index['name']:
				if (name in sys.argv):
					print ('Reseting the settings for '+name+'...')
					for filename in index['file']:
						print ('cp -vrf /home/'+userName+'/'+filename+' /home/'+userName+'/'+filename+'.backup')
						os.system('cp -vrf /home/'+userName+'/'+filename+' /home/'+userName+'/'+filename+'.backup')
					for folder in index['folder']:
						print ('cp -vrf /home/'+userName+'/'+folder+' /home/'+userName+'/'+folder[:len(folder)-1]+'.backup/')
						os.system('cp -vrf /home/'+userName+'/'+folder+' /home/'+userName+'/'+folder[:len(folder)-1]+'.backup/')
	elif ((('r' == temp[0])) or (('restore' == temp[0]))):
		defaultRun = False
		userName = os.popen('whoami').readline().split('\n')[0]
		# for running a preset this will restore specific user settings based on the presets config file that have been backed up with the backup command
		data = getSettings()
		for index in data:
			for name in index['name']:
				if (name in sys.argv):
					print ('Reseting the settings for '+name+'...')
					for filename in index['file']:
						print ('cp -vrf /home/'+userName+'/'+filename+'.backup /home/'+userName+'/'+filename)
						os.system('cp -vrf /home/'+userName+'/'+filename+'.backup /home/'+userName+'/'+filename)
					for folder in index['folder']:
						print ('cp -vrf /home/'+userName+'/'+folder[:len(folder)-1]+'.backup/. /home/'+userName+'/'+folder)
						os.system('cp -vrf /home/'+userName+'/'+folder[:len(folder)-1]+'.backup/. /home/'+userName+'/'+folder)
if defaultRun == True:# by default run the program for the current user but confirm operation
	if ((('f' == temp[0])) or (('force' == temp[0]))):
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
			if ((('b' == temp[0])) or (('backup' == temp[0]))):
				os.system('cp ')
			resetSettings(userName)
			print '#####################################################'
			print 'PLEASE REBOOT THE SYSTEM TO FINALIZE THE RESET!'
			print '#####################################################'
			print 'NOTE: You may be able to logout and back in to reset'
			print '      the changes, although it is still recomended'
			print '      to do a full reboot.'
			print '#####################################################'



exit()
exit()
exit()


# change font and icon theme
files = os.listdir('/home')
# for each users home directory
for fileName in files:
	####################################################################
	# create folders for user icons, themes, and fonts
	makeDir(os.path.join('/home',fileName,'.icons'))
	makeDir(os.path.join('/home',fileName,'.themes'))
	makeDir(os.path.join('/home',fileName,'.fonts'))
	####################################################################
	# update sources and activate getdeb repos
	sourcesfile = [] # sources for /etc/apt/sources.list.d/official-package-repositories.list
	sourcesfile.append(['deb http://packages.linuxmint.com olivia main','deb http://packages.linuxmint.com olivia main upstream import backports'])
	sourcesfile.append(['deb http://archive.ubuntu.com/ubuntu raring main','deb http://archive.ubuntu.com/ubuntu raring main restricted universe multiverse'])
	sourcesfile.append(['deb http://archive.ubuntu.com/ubuntu raring-updates main','deb http://archive.ubuntu.com/ubuntu raring-updates main restricted universe multiverse'])
	sourcesfile.append(['deb http://security.ubuntu.com/ubuntu/ raring-security main','deb http://security.ubuntu.com/ubuntu/ raring-security main restricted universe multiverse'])
	sourcesfile.append(['deb http://archive.canonical.com/ubuntu/ raring partner','deb http://archive.canonical.com/ubuntu/ raring partner'])
	# sets up software sources stack
	filePath = os.path.join('/etc','apt','sources.list.d','offical-package-repositories.list')
	if os.path.exists(filePath):
		# split the config file by lines into an array to loop though
		tempConfig=loadFile(filePath).split('\n')
		newConfig = '' # stores the new file as a string
		for line in tempConfig:
			foundString = False # this is used to prevent double line writes
			for item in sourcesfile:
				if line.find(item[0]) != -1:
					# write new setting and remove old one
					newConfig += item[1]+'\n'
					foundString = True
			if foundString == False:
				newConfig += line+'\n'
		writeFile(filePath,newConfig.replace('\n\n','\n'))
		# dedupe the lines in the file
		writeFile(filePath,'\n'.join(list(sorted(set(loadFile(filePath).split('\n'))))))
	print 'Software sources have been set!'
	####################################################################
	# write line to file
	writeFile('/etc/apt/sources.list',(loadFile('/etc/apt/sources.list')+'\ndeb http://archive.getdeb.net/ubuntu raring-getdeb apps games'))
	additionalsources = [] # sources for /etc/apt/sources.list
	additionalsources.append(['deb http://archive.getdeb.net/ubuntu raring-getdeb','deb http://archive.getdeb.net/ubuntu raring-getdeb apps games'])
	# set the file path
	filePath = os.path.join('/etc','apt','sources.list')
	if os.path.exists(filePath):
		# split the config file by lines into an array to loop though
		tempConfig=loadFile(filePath).split('\n')
		newConfig = '' # stores the new file as a string
		for line in tempConfig:
			foundString = False # this is used to prevent double line writes
			for item in additionalsources:
				if line.find(item[0]) != -1:
					# write new setting and remove old one
					newConfig += item[1]+'\n'
					foundString = True
			if foundString == False:
				newConfig += line+'\n'
		writeFile(filePath,newConfig.replace('\n\n','\n'))
		# dedupe the lines in the file
		writeFile(filePath,'\n'.join(list(sorted(set(loadFile(filePath).split('\n'))))))
		# make user the owner of this file once more since root is editing the files
	print 'Software sources have been set!'
	####################################################################
	# Configure Theme For Icons, and Fonts
	newSettingsArray = []
	# in this array the 0th value is searched for and if found the 1th 
	# value is used to replace the current line in the file
	newSettingsArray.append(['    <property name="IconThemeName" type="string" value="NITRUX"/>',''])
	newSettingsArray.append(['    <property name="IconThemeName" type="string"','    <property name="IconThemeName" type="string" value="NITRUX"/>'])
	newSettingsArray.append(['    <property name="FontName" type="string" value="Hermit Medium 12"/>',''])
	newSettingsArray.append(['    <property name="FontName" type="string"','    <property name="FontName" type="string" value="Hermit Medium 12"/>'])
	# sets up shortcuts for all users on the system
	filePath = os.path.join('/home',fileName,'.config','xfce4','xfconf','xfce-perchannel-xml','xsettings.xml')
	if os.path.exists(filePath):
		# split the config file by lines into an array to loop though
		tempConfig=loadFile(filePath).split('\n')
		newConfig = '' # stores the new file as a string
		for line in tempConfig:
			foundString = False # this is used to prevent double line writes
			for item in newSettingsArray:
				if line.find(item[0]) != -1:
					# write new setting and remove old one
					newConfig += item[1]+'\n'
					foundString = True
			if foundString == False:
				newConfig += line+'\n'
		writeFile(filePath,newConfig.replace('\n\n','\n'))
		# make user the owner of this file once more since root is editing the files
		os.system(('chown '+fileName+' '+filePath))
	print 'Icon Theme Set to NITRUX, font set to Hermit'
	########################################################################
	# change the desktop background
	newSettingsArray = []
	# in this array the 0th value is searched for and if found the 1th 
	# value is used to replace the current line in the file
	newSettingsArray.append(['        <property name="image-path" type="string" value="/usr/share/pixmaps/hackbox/wallpaperBranded.png"/>',''])
	newSettingsArray.append(['        <property name="image-path" type="string"','        <property name="image-path" type="string" value="/usr/share/pixmaps/hackbox/wallpaperBranded.png"/>'])
	# sets up shortcuts for all users on the system
	filePath = os.path.join('/home',fileName,'.config','xfce4','xfconf','xfce-perchannel-xml','xfce4-desktop.xml')
	if os.path.exists(filePath):
		# split the config file by lines into an array to loop though
		tempConfig=loadFile(filePath).split('\n')
		newConfig = '' # stores the new file as a string
		for line in tempConfig:
			foundString = False # this is used to prevent double line writes
			for item in newSettingsArray:
				if line.find(item[0]) != -1:
					# write new setting and remove old one
					newConfig += item[1]+'\n'
					foundString = True
			if foundString == False:
				newConfig += line+'\n'
		writeFile(filePath,newConfig.replace('\n\n','\n'))
		# make user the owner of this file once more since root is editing the files
		os.system(('chown '+fileName+' '+filePath))
	print 'desktop background is now setup correctly'
	####################################################################
	# install programs used for custom actions
	os.system('sudo apt-get install woof gimp audacity --assume-yes')
	# copy the thunar custom actions file over to each user
	if os.path.exists(os.path.join('/home',fileName,'.config','Thunar','uca.xml')):
		shutil.copy('resources/uca.xml',os.path.join('/home',fileName,'.config','Thunar','uca.xml'))
		os.system(('sudo chown '+fileName+' '+os.path.join('/home',fileName,'.config','Thunar','uca.xml')))
	# open port used for lan share of files using thunar
	os.system('sudo ufw allow from 192.168.1.0/24 to any port 9119')
	os.system('sudo ufw allow from 192.168.2.0/24 to any port 9119')
	####################################################################
	# setup the configuration for qshutdown for user
	if os.path.exists(os.path.join('/home',fileName,'.qshutdown')):
		configFilePath = os.path.join('/home',fileName,'.qshutdown','qshutdown.conf')
		print 'Setting up configuration for qshutdown...'
		programFile = loadFile(configFilePath).split('\n')
		temp = ''
		switch = True
		print 'Reading Config file...'
		# scan the config file to make shure the changes prepared have
		# not already been applyed
		for i in programFile:
			if i == 'Quit_on_close=true':
				switch = False
		# close file to reset and prepare for rewrite
		if switch == True:
			for i in programFile:
				if i == 'Quit_on_close=false':
					temp += 'Quit_on_close=true'
				else:
					temp += i
			print 'Editing Config file...'
			writeFile(configFilePath,temp)
			print 'Done working on config file!'
		else:
			print 'Config File already Correct!'
			print 'Moving along...'
		os.system(('chown '+fileName+' '+configFilePath))
	####################################################################
	# setup the configuration for xarchiver for user
	if os.path.exists(os.path.join('/home',fileName,'.config','xarchiver')):
		configFilePath = os.path.join('/home',fileName,'.config','xarchiver','xarchiverrc')
		print 'Setting up configuration for xarchiver...'
		programFile = loadFile(configFilePath).split('\n')
		temp = ''
		switch = True
		print 'Reading Config file...'
		# scan the config file to make shure the changes prepared have
		# not already been applyed
		for i in programFile:
			if i == 'show_sidebar=true':
				switch = False
		# close file to reset and prepare for rewrite
		if switch == True:
			for i in programFile:
				if i == 'show_sidebar=false':
					temp += 'show_sidebar=true'
				else:
					temp += i
			print 'Editing Config file...'
			writeFile(configFilePath, temp)
			print 'Done working on config file!'
		else:
			print 'Config File already Correct!'
			print 'Moving along...'
		os.system(('chown '+fileName+' '+configFilePath))
	####################################################################
	# configure transmission settings automaticly for user conveience+security
	if os.path.exists(os.path.join('/home',fileName,'.config','transmission')):
		configFilePath = os.path.join('/home',fileName,'.config','transmission','settings.json')
		import json
		programFile = json.load(open(configFilePath,'r'))
		programFile['blocklist-enabled'] = True
		programFile['blocklist-updates-enabled'] = True
		programFile['blocklist-url'] = "http://www.bluetack.co.uk/config/level1.gz"
		programFile['encryption'] = 2
		programFile['peer-port-random-on-start'] = True
		programFile['trash-orignal-torrent-files'] = True
		programFile['watch-dir-enabled'] = True
		programFile['watch-dir'] = '~/Downloads/'
		temp = open(configFilePath,'w')
		temp.write(json.dumps(programFile))
		temp.close()
		os.system(('chown '+fileName+' '+configFilePath))
	####################################################################
	#~ # setup mime types for system
	#~ cp fehOpen.desktop ~/.local/share/applications/ -v
	#~ cp ffplayOpen.desktop ~/.local/share/applications/ -v
	#~ cp mimeapps.list ~/.local/share/applications/ -v
	#~ # setup the support program fehOpen
	#~ pycompile ./supportPrograms/fehOpen.py
	#~ cp ./supportPrograms/fehOpen.pyc ./supportPrograms/fehOpen
	#~ sudo chmod +x ./supportPrograms/fehOpen
	#~ sudo cp ./supportPrograms/fehOpen /usr/bin/fehOpen
	#~ rm ./supportPrograms/fehOpen
	#~ rm ./supportPrograms/fehOpen.pyc
	
	#~ if os.path.exists(os.path.join('/home',fileName,'.config','transmission','blocklists')):
		#~ 
		#~ shutil.copy('./resources/uca.xml',
		#~ 
		#~ print 'Copy blocklist to',os.path.join('/home',fileName,'.config','transmission','blocklists')
		#~ copy(os.path.join(tempPath,'compiledBlocklist'),os.path.join('/home',fileName,'.config','transmission','blocklists'))
		#~ # if config folder exists edit config file for transmission
		#~ tempData = json.loads(loadFile(os.path.join('/home',fileName,'.config','transmission','settings.json')))
		#~ # require encryption
		#~ tempData['encryption'] = 2
		#~ # enable the blocklist
		#~ tempData['blocklist-enabled'] = True
		#~ # show the icon in the system tray
		#~ tempData['show-notification-area-icon'] = True
		#~ # write the config file with its changes
		#~ writeFile(os.path.join('/home',fileName,'.config','transmission','settings.json'),json.dumps(tempData))
