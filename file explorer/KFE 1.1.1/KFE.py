import os
import shutil
import stat
from time import sleep


class FileExplorer:
	def __init__(self):
		self.STARTPATH = os.environ['USERPROFILE']
		self.currentPath = self.STARTPATH
		self.files = []
		# TEXTS
		self.INPUTTEXT = '''\n# :back to revert to previous folder       #\n# :delete [file] to delete a file          #\n# :newfile [filename] to create a new file #\n# :movefile [from] [to] to move a file     #\n   >'''

		# COMMANDS
		self.COMMANDS = {
			':back': self.goBack,
			':delete': self.delete, ':newfile': self.newFile,
			':movefile': self.moveFile,

		}
		
	def main(self):
		try:
			self.files = os.listdir(self.currentPath)
		except PermissionError:
			print('\nSeems like you don\'t have the permission to open that file or directory')
			sleep(1.5)

		os.system('cls')

		for file in self.files:
			_, _, isHidden = self.pathExists_pathIsDirectory_pathIsHidden(file)
			if not isHidden:
				print(file)

		self.getInput()


	def getInput(self):
		inpTxt = input(self.INPUTTEXT)
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
						print('\nSomething went wrong trying to open the program')
						sleep(1.5) 
			else:
				print('\nYou tried to access a hidden file')
				sleep(1.5)
		else:
			print('\nFile or directory with that name doesn\'t exist')
			sleep(1.5)


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


	def correctPath(self):
		self.currentPath = self.currentPath.replace('/', '\\')
	


	def delete(self, command):
		os.system('cls')
		try:
			if os.path.exists(os.path.join(self.currentPath, command[1])):
				if input(f'Are you sure you want to permanently delete {command[1]} (Y - N)   >').lower() == 'y':
					if os.path.isdir(os.path.join(self.currentPath, command[1])):
						try:
							shutil.rmtree(os.path.join(self.currentPath, command[1]))
						except PermissionError:
							print('Seems like you don\'t have the permission to delete that file or directory')
							sleep(1.5)
					else:
						os.remove(os.path.join(self.currentPath, command[1]))

			else:
				print('File or directory with that name doesn\'t exist')
				sleep(1.5)
		except IndexError:
			print('You didnt\'t specify a path')
			sleep(1.5)


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
						print('\nFailed to write the file.')
				file.close()
		else:
			print('\nYou didn\'t specify a path')
			sleep(1.5)
	
	def moveFile(self, command):
		os.system('cls')
		try:
			shutil.move(os.path.join(self.currentPath, command[1]), os.path.join(self.currentPath, command[2]))
		except FileNotFoundError:
			print('File or directory you\'re trying to move doesnt exist')
			sleep(1.5)
		except shutil.Error:
			print('An error occured while moving the file.')
			sleep(1.5)

core = FileExplorer()

while True:
	core.main()
