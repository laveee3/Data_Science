import sys
import pandas as pd
from fuzzywuzzy import fuzz

df_sample = pd.read_csv('dample.csv')
df_addr_csv = df_sample[['EID','Address1','City','State','Zip Code']]
df_addr_csv = df_addr_csv[df_addr_csv['EID'].notna()]
df_addr_csv.sort_values(by=['EID'], inplace=True)
df_addr_csv = df_addr_csv.drop_duplicates()
#print(df_addr_csv)
raw_eid = df_addr_csv['EID'].dropna()
eid = raw_eid.tolist()

import cx_Oracle
connection = cx_Oracle.connect("xxxxx/xxxx@yyyyyys.com:9999/xxxxx.yyyy.com")
cursor = connection.cursor()
cursor.execute("select EID, addr_line1, addr_line2, city, state,zip from cips_main m, cips_addresses a  where m.ALUMNI_ID = a.ALUMNI_ID AND m.ut_eid IN %s" % str(tuple(eid)).replace(',)',')'))
df_addr_db = cursor.fetchall()
cursor.close()
connection.close()

df_addr_db = pd.DataFrame(df_addr_db, columns = ['EID','Address1','Address2','City','State','Zip Code'])
#dropping duplicates
df_addr_db = df_addr_db.drop_duplicates()
df_addr_db = df_addr_db[df_addr_db['Address1'].notna()]

addr_diff = pd.DataFrame()
for i in range(len(df_addr_csv)):
    flag = 0
    id_csv = df_addr_csv.iloc[i, 0]
    csv_addr = df_addr_csv.iloc[i, 1]
    cmp_dbaddr = df_addr_db.loc[df_addr_db['EID'] == id_csv]

    for j in range(len(cmp_dbaddr)):
        db_addr = cmp_dbaddr.iloc[j, 1]
        Token_Set_Ratio = fuzz.token_set_ratio(csv_addr, db_addr)
        if (Token_Set_Ratio > 77):
            flag = 0
            break
        else:
            flag = 1
    if (flag == 1):
        addrlist = []
        for k in range(len(cmp_dbaddr)):
            temp = (cmp_dbaddr.loc[cmp_dbaddr['EID'] == id_csv]).iloc[:, 1]
            addrlist = temp.values.tolist()
        addr_diff = addr_diff.append({'EID': id_csv, 'DB_Address': addrlist, 'CSV_Address': csv_addr},
                                     ignore_index=True)
#print("----------------------------------------------------------------")
#print(addr_diff)
#print("----------------------------------------------------------------")
addr_diff.to_csv(r'C:\Users\le5752\Documents\DB_Python\addr.csv', index = False)

#bar graph
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
variable = ['Input:CSV', 'DB_match']
count = [len(df_addr_csv),len(addr_diff)]
ax.bar(variable, count)
plt.show()