from cx_Oracle import *
from traceback import *

conn=None

class Db_Model():

    def __init__(self):
        self.file_dict={}
        self.db_status=True
        self.conn=None
        self.cur=None
        try:
            self.conn=connect("mymojo/mymojo@127.0.0.1/xe")
            print("Connected Successfully ")
            self.cur=self.conn.cursor()
        except:
            self.db_status=False
            print("DB Error", format_exc)

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()

        if self.conn is not None:
            self.conn.close()
        print("Disconnected Successfully")

    def add_file(self,file_name,file_path,file_owner,file_pwd):
        self.file_dict[file_name]= (file_path,file_owner,file_pwd)
        print("File Added:",self.file_dict[file_name])

    def get_file_path(self,file_name):
        return self.file_dict[file_name][0]

    def add_file_to_db(self,file_name,file_path,file_owner,file_pwd):
        self.cur.execute("select max(file_id) from mysecurefiles")
        max_id=self.cur.fetchone()
        if max_id[0]==None:
            max_id[0]=0
        #print(max_id)
        nxt_id=1
        if max_id is not None:
            nxt_id+=int(max_id[0])

        self.cur.execute("insert into mysecurefiles values(:1,:2,:3,:4,:5)",(nxt_id,file_name,file_path,file_owner,file_pwd))
        self.conn.commit()
        return"File affected  in Database"

    def load_files_from_db(self):
        self.cur.execute("select file_name,file_path,file_owner,file_pwd from mysecurefiles")
        record_added = False
        for file_name,file_path,file_owner,file_pwd in self.cur:
            self.file_dict[file_name]=(file_path,file_owner,file_pwd)
            record_added=True
        if record_added==True:
            return "File populated from Database"
        else:
            return "No file present in Database"

    def remove_files_from_db(self,file_name):
        self.cur.execute("delete from mysecurefiles where file_name=:1",(file_name,))
        if self.cur.rowcount==0:
            return "file not found in Database"
        else:
            self.file_dict.pop(file_name)
            self.conn.commit()
            return "File removed from Database"

    def is_file_secure(self,file_name):
        return file_name in self.file_dict

    def get_file_pwd(self,file_name):
        return self.file_dict[file_name][2]

    def get_file_count(self):
        return len(self.file_dict)

