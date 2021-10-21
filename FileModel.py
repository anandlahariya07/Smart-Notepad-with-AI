import string
from tkinter.filedialog import *

class File_Model():

    def __init__(self):
        self.key= string.ascii_lowercase+string.ascii_uppercase+string.digits
        self.offset=7
        self.url=""

    def encrypt(self, plaintext):
        result=""
        try:
            for l in plaintext:
                ind=(self.key.index(l)+self.offset)%62
                result+=self.key[ind]
        except ValueError:
            result+=l
        return result

    def decrypt(self, ciphertext):
        result = ""
        try:
            for l in ciphertext:
                ind = (self.key.index() - self.offset) % 62
                result += self.key[ind]
        except ValueError:
            result += l
        return result

    def open_file(self):
        self.url=askopenfilename(title="Select file",filetypes=[("Text Documents","*.")])

    def new_file(self):
        self.url=""

    def save_as(self,msg):
        encrypted_text=self.encrypt(msg)
        self.url=asksaveasfile(mode="w", defaultextension='.ntxt', filetypes=[("All Files","*.*"),("Text Document",".txt")])
        self.url.write(encrypted_text)
        filepath=self.url.name
        self.url.close()
        self.url=filepath

    def save_file(self,msg):
        if self.url=="":
            self.url=asksaveasfilename(title="Select file Name", defaultextension='.ntxt', filetypes=[("Text Documents",".txt")])
        file_name,file_extension= os.path.splitext(self.url)

        if file_extension=='.ntxt':
                msg=self.encrypt(msg)
        with open(self.url,"w",encoding="utf-8") as fw:
                fw.write(msg)

    def read_file(self,url=''):
        if url!='':
            self.url=url
        else:
            self.open_file()
        base=os.path.basename(self.url)
        file_name, file_extension=os.path.splitext(self.url)
        fr=open(self.url,"r")
        contents=fr.read()
        if file_extension=='.ntxt':
            contents=self.decrypt(contents)
        fr.close()
        return contents, base
