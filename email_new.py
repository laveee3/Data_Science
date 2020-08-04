import sys
import pandas as pd
df_sample = pd.read_csv('dample.csv')
#print(df_sample[['EID','Email Address','Home Phone','Address1', 'City', 'State', 'Zip Code']])

# -------- Email Diff ---------
df_csv = df_sample[['EID','Email Address']]
df_csv.sort_values(by=['EID'], inplace=True)
df_csv = df_csv.dropna()
raw_eid = df_csv['EID'].dropna()
#print(raw_eid)
eid = raw_eid.tolist()
#print(eid)

# Connect to Database
import cx_Oracle
connection = cx_Oracle.connect("xxxxx/xxxx@yyyyyys.com:9999/xxxxx.yyyy.com")
cursor = connection.cursor()
cursor.execute("select EID, lower(vi_email_addr) from cips_main m, cips_email_info e where m.ALUMNI_ID = e.ALUMNI_ID AND m.ut_eid IN %s" % str(tuple(eid)).replace(',)',')'))
results = cursor.fetchall()
df_db = results
cursor.close()
connection.close()


df_db = pd.DataFrame(results, columns = ['EID','Email Address'])
df_db_nodup = df_db.drop_duplicates()

df_email = pd.DataFrame()
for i in range(len(df_csv)):
    id_csv = df_csv.iloc[i,0]
    email_csv = df_csv.iloc[i,1]
    email_db = (df_db.loc[df_db['EID'] == id_csv]).iloc[:,1]
    email_csv=email_csv.lower()
    email_db = {*email_db}
    email_csv = {email_csv}
    diff = (email_csv - email_db)
    if len(diff) > 0:
        df_email = df_email.append({'EID':id_csv, 'Email':df_csv.iloc[i,1]}, ignore_index=True)

df_email = df_email.drop_duplicates()
df_email['DB_email'] = ''
for i in range(len(df_email)):
    id_csv = df_email.iloc[i, 0]
    e_db = (df_db.loc[df_db['EID'] == id_csv]).iloc[:, 1]
    df_email.iloc[i, 2] = e_db.values.tolist()

df_email.to_csv(r'C:\Users\le5752\Documents\DB_Python\eee.csv', index=False)