# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:22:11 2022


Default users password : P@ssw0rd
"""

import sqlite3
import pandas as pd
import datetime
import time

def convert_into_binary(file_path):
    with open(file_path, 'rb') as file:
        binary = file.read()
    return binary

class DBO:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('test.db', check_same_thread=False)
            self.cur = self.conn.cursor()
            # check if table exists
            print('[*] Checking if USERS table exists in the database:')
            self.listOfTables = self.cur.execute(
                """SELECT name FROM sqlite_master WHERE type='table'
                AND name='USERS'; """).fetchall()
     
            if self.listOfTables == []:
                print('[-] USERS Table does not exist : Creating with default entries.')
                self.init_table()
            else:
                print('[+] USERS Table found!')
                
        except Exception as e:
            print(e)
            
            
            
    def init_table(self):
        try:
            self.cur.execute(
                """CREATE TABLE USERS(USERNAME VARCHAR(30),FNAME VARCHAR(30),LNAME VARCHAR(30),
                ROLE VARCHAR(15), PASSWORD VARCHAR(64));""")
            self.conn.commit()
            print('[+] USERS table created')
            
            self.conn.execute("""INSERT INTO USERS (USERNAME,FNAME,LNAME,ROLE,PASSWORD)
                         VALUES ('admin', 'admin','admin', 'admin', '205f0f3ff2d9531c54cb61ceb7bed9db11cb7a9a56b654d8d1efc6982f50122e')""")
            self.conn.commit()
            print('[+] Admin user created')
            self.conn.execute("""INSERT INTO USERS (USERNAME,FNAME,LNAME,ROLE,PASSWORD)
                         VALUES ('analyst', 'analyst', 'analyst', 'analyst', '166b29b136583748cdeda22b3abeb11aecc60d8d2fd0b9046011b31cebc0fdc4')""")
            self.conn.commit()
            print('[+] Analyst user created')
            
            print('[+] Default users created')
            
            query= """CREATE TABLE equipment_master        
            (    Type varchar(255),
                EQUIPMENT_NAME varchar(255),
                MAKE varchar(255),
                MODEL_NUMBER varchar(255),
                SR_NO_ID varchar(255),
                DONE_DATE varchar(255),
                DUE_DATE varchar(255),
                STATUS varchar(255),
                ISSUED_TO varchar(255),
                COMPANY_NAME varchar(255),
                REMARK varchar(255))"""
            self.conn.execute(query)
            self.conn.commit()
            
            query= """INSERT INTO equipment_master        
               (Type,EQUIPMENT_NAME ,MAKE ,
                MODEL_NUMBER,SR_NO_ID,DONE_DATE ,
                DUE_DATE ,STATUS ,ISSUED_TO,COMPANY_NAME,
                REMARK) VALUES ('','','',
                '','','','','','','','')"""
            self.conn.execute(query)
            self.conn.commit()
            
           
            print('[+] Equioment Table users created')    
            query= """CREATE TABLE company_details        
                        (    
                             COMPANY_NAME varchar(255),
                             ADDRESS varchar(255),
                             REPORT_NUMBER varchar(255))"""
            self.conn.execute(query)
            self.conn.commit()
            
            query = """INSERT INTO company_details 
             ('COMPANY_NAME', 'ADDRESS', 'REPORT_NUMBER') 
             VALUES ( '{}','{}','{}')""".format("","","")
            self.conn.execute(query)
            self.conn.commit()

            
            print('[+] Customer Table users created')
            
            query= """CREATE TABLE elogbook        
            (    
                SR_NO_ID varchar(255),
                STATUS varchar(255),
                ISSUED_TO varchar(255),
                COMPANY_NAME varchar(255),
                REMARK varchar(255),
                update_time varchar(255))"""
    
            self.conn.execute(query)
            self.conn.commit()
            
            print('[+] ElogBook Table users created')
            
            
            
            
            return 0
        except Exception as e:
            return e
        
        
    def create_user(self, username,fname,lname, role, password):
        try:             
            query = """INSERT INTO USERS ( USERNAME ,FNAME,LNAME ,ROLE, PASSWORD)
                         VALUES ( '{}','{}','{}','{}','{}')""".format(username,fname,lname,role,password)
            self.conn.execute(query)
            self.conn.commit()
            return 0
        except Exception as e:
            return e
        
    
    def delete_user(self, username):
        try:
            if username not in ('admin', 'analyst'):
                self.conn.execute("DELETE from USERS where USERNAME = '" + username + "'")
                self.conn.commit()
                print("Number of users deleted :", self.conn.total_changes)
            else:
                print("[-] Error : Cannot delete default users.")
            return 0
        except Exception as e:
            return e

        
    def get_cred(self, username):
        try:
            stmt = "SELECT ROLE, PASSWORD,FNAME,LNAME from USERS where USERNAME = '" + username + "'"
            cursor = self.conn.execute(stmt)
            ret_obj = {"role": "", "password": ""}
            for row in cursor:
                print("inside cur loop")
                ret_obj["role"] = row[0]
                ret_obj["password"] = row[1]
                ret_obj["username"] = row[2]+" "+row[3]
                break
            return ret_obj
        except Exception as e:
            print(e)
            return e
        
    
    def update_user(self, username, role, password):
        try:
            self.conn.execute("UPDATE USERS set PASSWORD = " + password + ", ROLE = " + role + " where USERNAME = '" + username + "'")
            self.conn.commit()
            print("[+] Password updated :", self.conn.total_changes)
            return 0
        except Exception as e:
            return e  
            
    #################################### Start Of Euipment query #########################################################        
    def get_equipment(self):
        try:
            stmt = "SELECT * from equipment_master "
            cursor = self.conn.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            
            return equipment_frame
        except Exception as e:
            return e
            
    def get_equipment_by_id(self,SR_NO_ID):
        try:
            stmt = "SELECT * from equipment_master where SR_NO_ID='{}'".format(SR_NO_ID)
            cursor = self.conn.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list)
            equipment_frame.columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK']
            return equipment_frame
        except Exception as e:
            return e
            
    def get_logBook(self):
        try:
            stmt = "SELECT * from elogbook "
            cursor = self.conn.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['SR_NO_ID' ,'STATUS','ISSUED_TO' ,'COMPANY_NAME' , 'REMARK' ,'update_time'])
            return equipment_frame
        except Exception as e:
            return e
            
    def get_available_equipment(self):
        try:
            stmt = "SELECT * from equipment_master where status='AVAILABLE' OR status='CLOSED'"
            cursor = self.conn.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            return equipment_frame
        except Exception as e:
            return e
            
    def get_penidng_for_approval_equipment(self):
        try:
            stmt = "SELECT * from equipment_master where status='REQUESTED'"
            cursor = self.conn.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            return equipment_frame
        except Exception as e:
            return e
            
    def selected_instrument_dropdown(self,TYPE,ISSUED_TO):
        try:
            stmt = """SELECT * from equipment_master where
            status='APPROVED' and Type='{}' and ISSUED_TO='{}'""".format(TYPE,ISSUED_TO)
            cursor = self.conn.execute(stmt)
            equipment_list = []
            for row in cursor:
                equipment_list.append(list(row))
            equipment_frame = pd.DataFrame(equipment_list,columns = ['Type' ,'EQUIPMENT_NAME' ,'MAKE' ,'MODEL_NUMBER','SR_NO_ID' ,'DONE_DATE' ,'DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK'])
            return equipment_frame
            
        except Exception as e:
            return e       

    def request_for_equipment(self,SR_NO_ID,company_name,REMARK,ISSUED_TO):
        try:
            stmt = """update equipment_master 
                      set STATUS= 'REQUESTED' , ISSUED_TO='{}' ,COMPANY_NAME='{}' ,REMARK='{}'
                      where SR_NO_ID='{}' """.format(ISSUED_TO,company_name,REMARK,SR_NO_ID)
            cursor = self.conn.execute(stmt)
            self.conn.commit()
            ts = time.time()
            update_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')       
            print(update_time)           
            query = """INSERT INTO elogbook 
                    (SR_NO_ID ,STATUS,ISSUED_TO ,COMPANY_NAME , REMARK ,update_time) 
                    VALUES ( '{}','{}','{}','{}','{}','{}')""".format(SR_NO_ID,'REQUESTED',ISSUED_TO,company_name,REMARK,update_time)
            cursor = self.conn.execute(query)
            self.conn.commit()
            
        except Exception as e:
            return e 
            
    def update_request_for_equipment(self,temp_Df,ISSUED_TO):
        try:
            for row in temp_Df.itertuples():
                STATUS = row[2]
                if STATUS=="APPROVED":
                    stmt = """update equipment_master 
                              set STATUS= '{}'  ,REMARK='{}' 
                              where SR_NO_ID='{}' """.format(row[2],row[3],row[1])
                    cursor = self.conn.execute(stmt)
                    self.conn.commit()
                
                    ts = time.time()
                    update_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')            
                    query = """INSERT INTO elogbook 
                            (SR_NO_ID ,STATUS,ISSUED_TO ,COMPANY_NAME , REMARK ,update_time) 
                            VALUES ( '{}','{}','{}','{}','{}','{}')""".format(row[1],STATUS,ISSUED_TO,row[4],row[3],update_time)
                    cursor = self.conn.execute(query)
                    self.conn.commit()
            
        except Exception as e:
            return e             
            
    def update_equipment(self,equipment_master):
        try:
            self.conn.execute("""DELETE  FROM  equipment_master""")
            self.conn.commit()
            for row in equipment_master.itertuples():
                query = """INSERT INTO equipment_master 
                    (Type ,EQUIPMENT_NAME ,MAKE ,MODEL_NUMBER,SR_NO_ID ,
                    DONE_DATE ,DUE_DATE,STATUS,ISSUED_TO ,COMPANY_NAME,REMARK) 
                    VALUES ( '{}','{}','{}','{}','{}',
                   '{}','{}','{}','{}','{}','{}')""".format(row[1],row[2],row[3],row[4],
                                                  row[5],row[6],row[7],
                                                  row[8],row[9],row[10],row[11])
                self.conn.execute(query)
                self.conn.commit()
                
        except Exception as e: 
            return e
    ################################# Start Company Details Query ####################################################        
    def get_company_details(self):
        try:
            stmt = "SELECT * from company_details "
            cursor = self.conn.execute(stmt)
            company_list = []
            for row in cursor:
                company_list.append(list(row))
            company_frame = pd.DataFrame(company_list,columns = ['COMPANY_NAME', 'ADDRESS', 'REPORT_NUMBER'])
            return company_frame
        except Exception as e:
            return e
            
    def get_company_details_by_company_name(self,COMPANY_NAME):
        try:
            stmt = "SELECT * from company_details where COMPANY_NAME='{}'".format(COMPANY_NAME)
            cursor = self.conn.execute(stmt)
            company_list = []
            for row in cursor:
                company_list.append(list(row))
            company_frame = pd.DataFrame(company_list,columns = ['COMPANY_NAME', 'ADDRESS', 'REPORT_NUMBER'])
            return company_frame
        except Exception as e:
            return e
            
    def update_company_details(self,company_details):
        try:
            self.conn.execute("""DELETE  FROM  company_details""")
            self.conn.commit()
            for row in company_details.itertuples():
                query = """INSERT INTO company_details 
                    (COMPANY_NAME ,ADDRESS ,REPORT_NUMBER) 
                    VALUES ( '{}','{}','{}')""".format(row[1],row[2],row[3])
                self.conn.execute(query)
                self.conn.commit()
                
        except Exception as e: 
            return e            
    ################################# End Company Details Query ####################################################          
    
    def insert_file(self,file_name,file_path):
        try:
            table_name = "file_db"
            binary_file = convert_into_binary(file_path)
            sqlite_insert_blob_query = """INSERT INTO {} (name, data)
            VALUES ('{}', '{}')""".format(table_name,file_name,binary_file)
            print(sqlite_insert_blob_query)
            self.conn.execute(sqlite_insert_blob_query)
            self.conn.commit()
            print('File inserted successfully')
        except sqlite3.Error as error:
            print("Failed to insert blob into the table")
           
                