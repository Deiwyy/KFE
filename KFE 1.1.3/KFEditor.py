from tkinter import *
from tkinter import messagebox
import os

class Editor:
	def __init__(self, file, texts):
		self.texts = texts
		self.root = Tk()
		self.root.title('Kapa File Explorer')
		self.textField = Text(self.root)
		self.file = file

		if os.path.exists(self.file):
			with open(self.file, 'r') as file:
				for line in reversed(file.readlines()):
					self.textField.insert('1.0', line)
		
		self.textField.grid()
		self.saveButton = Button(text='Save', command = self.save).grid()
		self.main()


	def save(self):
		textToSave = self.textField.get('1.0', 'end-1c')
		try:
			with open(self.file, 'w') as file:
				file.write(textToSave)
		except PermissionError:
			messagebox.showinfo('Error', self.texts['noPermission'])


	def on_close(self):
		if messagebox.askokcancel('Quit', 'Do you want to quit? Any unsaved progress will be lost.'):
			self.root.destroy()


	def main(self):
		self.root.protocol('WM_DELETE_WINDOW', self.on_close)
		self.root.mainloop()

