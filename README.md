# BatchBuildLightUE4
[Python] [PyQt5] [UE4] [GameArt] [GameDev]

![Logo B-Blue](Resources/Logo-BBlue.png)
## Summary
Python tools [GUI] to automatize your *build light* process on UE4 project. This tools are in dev, it's functional but only for my project, a huge refactoring are needed to work for all project.

# Dependence
This tool use Python 3 and work with any package, more information are 
available with the *requirement.txt*. Quickly, see this list :
 - PyQt5
 - python-perforce (needed only to use P4, and not maintain with latest release)
 - psutil
 - ifaddr
 

# How to use
First step, you need to setup all path, you can find it on the Menu Bar 
*"Setup"*, when you have finished, youcan see your levels appeared on your 
main windows. Now, select your level(s) and click built-it.

 You can select the checkbox "All" to force your Swarm Agent to use more machine.

 !! Don't forget to disable your hibernate option from Windows !!

![Screen Capture](Resources/ScreenBatchBuildLight.jpg)

## FAQ
### What licence use this software

### How to setup the Network

~\BBLUE4\network.json

### How to Build
Launch a build packages inside the folder Builds, launch the Release.py 
files with python and use an absolute path like 
`X:/PathAboutThisFiles/Release.py` and don't forget to check the 7-zip path 
-inside the packages.bat.

Now, it's work only with PyCharm -setup an absolute path, and correctly use 
the module BatchBuildLight.