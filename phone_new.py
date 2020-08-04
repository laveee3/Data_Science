import sys
import re
import pandas as pd
df_sample = pd.read_csv('dample.csv')

df_ph_csv = df_sample[['EID','Home Phone']]
df_ph_csv = df_ph_csv[df_ph_csv['EID'].notna()] # drops only rows where eid column is na

#adding empty column
df_ph_csv['telephone'] = ''
raw_eid = df_ph_csv['EID'].dropna()
eid = raw_eid.tolist()
for i in range(len(df_ph_csv)) :
    #df_ph_csv.iloc[i,2]=re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',df_ph_csv.iloc[i,1])
    if pd.isnull(df_ph_csv.iloc[i,1]):
        continue
    df_ph_csv.iloc[i,2]=df_ph_csv.iloc[i,1].replace("(","").replace(")","").replace("-","").replace("/","")

import cx_Oracle
connection = cx_Oracle.connect("xxxxx/xxxx@yyyyyys.com:9999/xxxxx.yyyy.com")
cursor = connection.cursor()
cursor.execute("select EID, phone_area_code, phone_nbr from cips_main m, cips_phone_info p where m.ALUMNI_ID = p.ALUMNI_ID AND m.ut_eid IN %s" % str(tuple(eid)).replace(',)',')'))
results = cursor.fetchall()
df_ph_db = results
cursor.close()
connection.close()
#print(df_ph_db)
df_ph_db = pd.DataFrame(results, columns = ['EID','Area','phone'])
#dropping duplicates
df_ph_db = df_ph_db.drop_duplicates()
#print(df_ph_db)

df_ph_db["telephone"] = df_ph_db["Area"].astype(str) + df_ph_db["phone"].astype(str)
#print(df_ph_db)

df_phone = pd.DataFrame()
for i in range(len(df_ph_csv)):
    id_csv = df_ph_csv.iloc[i, 0]
    ph_csv = df_ph_csv.iloc[i, 2]
    ph_db = (df_ph_db.loc[df_ph_db['EID'] == id_csv]).iloc[:, 3]
    ph_db = {*ph_db}
    ph_csv = {ph_csv}
    diff = (ph_csv - ph_db)
    if len(diff) > 0:
        df_phone = df_phone.append({'EID': id_csv, 'telephone': df_ph_csv.iloc[i, 2]}, ignore_index=True)

df_phone = df_phone.drop_duplicates()

df_phone['DB_phone'] = ''
for i in range(len(df_phone)):
    id_csv = df_phone.iloc[i, 0]
    ph_db = (df_ph_db.loc[df_ph_db['EID'] == id_csv]).iloc[:, 3]
    df_phone.iloc[i, 2] = ph_db.values.tolist()

df_phone = df_phone[df_phone['telephone'].notna()]
df_phone['telephone'].dropna()
print(df_phone['telephone'].dropna())
