# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 20:23:25 2022

@author: Vivek
"""


from lib.db_dervices import DBO

dbo = DBO()

print(dbo.get_cred("admin"))