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
		print(self.currentPath)
		fileChoice = input('\n# @back to revert to previous folder #\n   >')

		if fileChoice == '@back':	
			self.goBack()

		elif os.path.exists(os.path.join(self.currentPath, fileChoice)):
			if os.path.isdir(os.path.join(self.currentPath, fileChoice)):
				self.currentPath = os.path.join(self.currentPath, fileChoice)
			else:
				os.startfile(os.path.join(self.currentPath, fileChoice), 'open')
		else:
			print('File or directory with that name doesn\'t exist')
			sleep(1.5)

	def goBack(self):
		splitPath = self.currentPath.split('\\')
		self.currentPath = 'C:\\'
		splitPath.pop(len(splitPath)-1)
		splitPath.pop(0)
		for a in splitPath:
			self.currentPath = os.path.join(self.currentPath, a)

core = FileExplorer()

while True:
	core.main() 