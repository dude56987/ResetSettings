ResetSettings
=============
Resets all settings for a specific user with defaults from /etc/skel or resets a single application for a specific user with defaults from /etc/skel.

####Unstable Package for Ubuntu and Linux Mint
https://github.com/dude56987/ResetSettings/blob/master/resetsettings_UNSTABLE.deb?raw=true

####Usage
    
    resetsettings
    
Using the command by itself will pull up a prompt requiring user to interact to proceed. This will reset all the settings for the current user to the defaults stored in /etc/skel.

    resetsettings -h
    
This will pull up a help menu similar to this section of the document you are reading.

    resetsettings -l
    
Lists all aplications available to be reset.

    resetsettings -p applicationName

Replace applicationName with one of the presets listed with the -l argument.

    resetsettings -u user1 user2 user3
    
Resets the settings for all listed users specified.
