import os
import shutil
import stat
from time import sleep


class FileExplorer:
	def __init__(self):
		self.errorSleepTime = 5
		self.STARTPATH = os.path.expanduser('~')
		self.currentPath = self.STARTPATH
		self.files = []

		self.texts = {
		'missingTxts': 'There are some missing texts in the txts.txt file, you can continue using this program, but expect bugs if you do'
		} # missingTxts by default here
		self.getTextsFromFile()

		# COMMANDS
		self.COMMANDS = {
			':back': self.goBack,
			':delete': self.delete, ':newfile': self.newFile,
			':movefile': self.moveFile,
			':copyfile': self.copyFile,

		}


	def getTextsFromFile(self):
		requiredTexts = ['inputText', 'noPermission', 'doesNotExist', 'error', 'fileHidden', 'pathNotSpecified']
		textsDirectory = './texts/'
		currentTxt = ''
		currentTxtName = ''
		readingAText = False
	
		with open(f'{textsDirectory}txts.txt') as textsFile:
			for line in textsFile:
				if line.startswith('-'):
					currentTxtName = line[1:].rstrip()
					readingAText = True
				elif line.rstrip() == '=':
					self.texts[currentTxtName] = currentTxt[:-1]
					readingAText = False
					currentTxt = ''				
				elif readingAText:
					currentTxt += line

		missingReqTxts = False
		for reqtxt in requiredTexts:
			if not reqtxt in self.texts:
				self.texts[reqtxt] = '-Missing text-'
				missingReqTxts = True

		if missingReqTxts:
			self.error(self.texts['missingTxt'])


	def error(self, msg):
		os.system('cls')
		print(msg)
		sleep(self.errorSleepTime)
		return
		

	def main(self):
		try:
			self.files = os.listdir(self.currentPath)
		except PermissionError:
			self.error(self.texts['noPermission'])


		os.system('cls')

		for file in self.files:
			_, _, isHidden = self.pathExists_pathIsDirectory_pathIsHidden(file)
			if not isHidden:
				print(file)

		self.getInput()


	def getInput(self):
		inpTxt = input(self.texts['inputText'])
		pathExists, pathIsDirectory, isHidden = self.pathExists_pathIsDirectory_pathIsHidden(inpTxt)

		if inpTxt.startswith(':'):
			inpTxt = inpTxt.split(' ')
			if inpTxt[0] in self.COMMANDS:
				self.COMMANDS[inpTxt[0]](inpTxt)

		elif pathExists:
			if not isHidden:
				if pathIsDirectory:
					self.currentPath = os.path.join(self.currentPath, inpTxt)
				else:
					try:
						os.startfile(os.path.join(self.currentPath, inpTxt), 'open')
					except OSError:
						self.error(self.texts['error']) 
			else:
				self.error(self.texts['fileHidden']) 
		else:
			self.error(self.texts['doesNotExist']) 


	def pathExists_pathIsDirectory_pathIsHidden(self, file):
		pathExists = os.path.exists(os.path.join(self.currentPath, file))
		pathIsDirectory = os.path.isdir(os.path.join(self.currentPath, file))
		if pathExists:
			pathIsHidden = bool(os.stat(os.path.join(self.currentPath, file)).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
		else:
			pathIsHidden = False
		return pathExists, pathIsDirectory, pathIsHidden


	def goBack(self, command):
		splitPath = self.currentPath.split('\\')
		self.currentPath = 'C:\\'
		splitPath.pop(len(splitPath)-1)
		splitPath.pop(0)
		for a in splitPath:
			self.currentPath = os.path.join(self.currentPath, a)


	def delete(self, command):		
		try:
			if os.path.exists(os.path.join(self.currentPath, command[1])):
				if input(f'Are you sure you want to permanently delete {command[1]} (Y - N)   >').lower() == 'y':
					if os.path.isdir(os.path.join(self.currentPath, command[1])):
						try:
							shutil.rmtree(os.path.join(self.currentPath, command[1]))
						except PermissionError:
							print(self.texts['noAccess'])
					else:
						os.remove(os.path.join(self.currentPath, command[1]))

			else:
				self.error(self.texts['doesNotExist']) 
		except IndexError:
			self.error(self.texts['pathNotSpecified']) 


	def newFile(self, command):
		if len(command) == 2 and command[1] != '':
			os.system('cls')
			fileText = ''
			writing = True
			print('leave a line blank to end writing the file\n')
			while writing:
				txt = input( ' >')
				if txt != '':
					fileText += txt + '\n' 
				else:
					writing = False
			
			saveTheFile = input('Save the file? (Y) > ').lower()

			if saveTheFile.lower() == 'y': 
				with open(os.path.join(self.currentPath, command[1]), 'w') as file:
					try:
						file.write(fileText)
					except UnicodeEncodeError:
						self.error(self.texts['error']) 
				file.close()
		else:
			self.error(self.texts['pathNotSpecified']) 

	
	def moveFile(self, command):
		try:
			shutil.move(os.path.join(self.currentPath, command[1]), os.path.join(self.currentPath, command[2]))
		except FileNotFoundError:
			self.error(self.texts['doesNotExist']) 
		except shutil.Error:
			self.error(self.texts['error'])
		except IndexError:
			self.error(self.texts['pathNotSpecified'])


	def copyFile(self, command):
		if len(command) >= 2:
			if os.path.exists(os.path.join(self.currentPath, command[1])) and command[2] != '':			
				if os.path.exists(os.path.join(self.currentPath, command[2])):
					try:
						shutil.copyfile(os.path.join(self.currentPath, command[1]), os.path.join(self.currentPath, command[2]))
					except shutil.Error:
						self.error(self.texts['error']) 
					except PermissionError:
						self.error(self.texts['noPermission']) 
				else:
					self.error(self.texts['doesNotExist']) 
			else:
				self.error(self.texts['doesNotExist']) 
		else:
			self.error(self.texts['pathNotSpecified']) 

core = FileExplorer()

while True:
	core.main()
