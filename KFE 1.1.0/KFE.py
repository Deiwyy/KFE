import os
import subprocess
from time import sleep


class FileExplorer:
	def __init__(self):
		self.STARTPATH = os.environ['USERPROFILE']
		self.currentPath = self.STARTPATH
		self.files = []

	def main(self):
		try:
			self.files = os.listdir(self.currentPath)
		except PermissionError:
			print('Seems like you don\'t have the permission to open that file or directory')
			sleep(1.5)

		os.system('cls')

		for file in self.files:
			print(file)
		
		command = input('\n# :back to revert to previous folder #\n   >')

		if command.startswith(':'):
			
			if command == ':back':	
				self.goBack()
			else:
				try:
					if command.split(' ')[0].lower() == ':delete' or ':newfile':
						command = command.split(' ')
						if command[0] == ':delete':
							self.delete(command[1])
						else:
							self.newFile(command[1])
				except IndexError:
					print('You didn\'t specify a file name')
				


		elif os.path.exists(os.path.join(self.currentPath, command)):
			if os.path.isdir(os.path.join(self.currentPath, command)):
				self.currentPath = os.path.join(self.currentPath, command)
			else:
				os.startfile(os.path.join(self.currentPath, command), 'open')
		else:
			print('File or directory with that name doesn\'t exist')
			sleep(1.5)
		self.correctPath()

	def goBack(self):
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
			if os.path.exists(os.path.join(self.currentPath, command)):
				if input(f'Are you sure you want to permanently delete {command} (Y - N)   >').lower() == 'y':
					try:
						os.remove(os.path.join(self.currentPath, command))
					except PermissionError:
						print('Seems like you don\'t have the permission to delete that file or directory')
						sleep(1.5)
			else:
				print('File or directory with that name doesn\'t exist')
				sleep(1.5)
		except IndexError:
			print('You didnt\'t specify a path')
			sleep(1.5)


	def newFile(self, command):
		os.system('cls')
		fileText = ''
		writing = True

		print('leave a line blank to end writing the file')
		while writing:
			txt = input( ' >')
			if txt != '':
				fileText += txt + '\n'
			else:
				writing = False
		
		saveTheFile = input('Save the file? (Y) > ').lower()

		if saveTheFile.lower() == 'y':
			with open(os.path.join(self.currentPath, command), 'w') as file:
				file.write(fileText)
			file.close()
		
core = FileExplorer()

while True:
	core.main()
