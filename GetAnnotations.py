#-*- coding: utf-8 -*-
import pyodbc
import pandas as pd

driver = 'SQL SERVER'
server = 'db.ntllab.com'
database = 'ai'
username = 'dev_team'
password = '!@#dnflsmsroqkfxla'

cnxn = pyodbc.connect('DRIVER={' + driver + '};server=' + server + ';database=' + database + ';UID=' + username + ';PWD=' + password +';')
cursor = cnxn.cursor()

sql = """
select d.dstFileName, v.json_roi
from DATASET_COPY_LIST d join v_learning_set v on d.idxCvg=v.idx_cvg and d.idxImg=v.idx_img
where v.idx_ai_model=48
and d.groupName='Acetowhite_P1B_trainset_20220325'
"""

cursor.execute(sql)
rows = cursor.fetchall()

# rows
df =pd.DataFrame(rows)
df.to_csv('./result.csv',mode='w',header=None,index=False)