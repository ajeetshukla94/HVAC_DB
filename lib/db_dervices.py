# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:22:11 2022

@author: Vivek

Default users password : P@ssw0rd
"""

import sqlite3

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
                """CREATE TABLE USERS(USERNAME VARCHAR(30),
                ROLE VARCHAR(15), PASSWORD VARCHAR(64));""")
            print('[+] USERS table created')
            
            self.conn.execute("""INSERT INTO USERS (USERNAME,ROLE,PASSWORD)
                         VALUES ('admin', 'admin', '29cac80ff6a0156263c5d414825633dd4175c77a67ff75f54860991e7c0e0bd0')""")
    
            self.conn.execute("""INSERT INTO USERS (USERNAME,ROLE,PASSWORD)
                         VALUES ('analyst', 'analyst', 'ce817ec2779be727aadd4e3b42fe850685341027852d97fc26fef783864fb2ec')""")
            self.conn.commit()
            print('[+] Default users created')
            return 0
        except Exception as e:
            return e
        
        
    def create_user(self, username, role, password):
        try:
            self.conn.execute("""INSERT INTO USERS (USERNAME,ROLE,PASSWORD)
                         VALUES (""" + username + """, 
                         """ + role + """, 
                         """ + password + """)""")
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
            stmt = "SELECT ROLE, PASSWORD from USERS where USERNAME = '" + username + "'"
            cursor = self.conn.execute(stmt)
            ret_obj = {"role": "", "password": ""}
            for row in cursor:
                print("inside cur loop")
                ret_obj["role"] = row[0]
                ret_obj["password"] = row[1]
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