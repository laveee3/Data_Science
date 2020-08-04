# importing pandas module
import pandas as pd

# making data frame
df_addr = pd.read_csv(r"C:\Users\Documents\DB_Python\addr.csv")
df_phone = pd.read_csv(r"C:\Users\Documents\DB_Python\ph.csv")
df_email = pd.read_csv(r"C:\Users\Documents\DB_Python\email_diff_July10.csv")
# df_email.head(10)
# df_phone.head(10)
# df_addr.head(10)
frames = [df_email, df_phone, df_addr]
# result = pd.concat(frames)
result = pd.merge(df_email, df_phone, how='outer');
result1 = pd.merge(df_addr, result, how='outer');
result1.to_csv(r'C:\Users\Documents\DB_Python\Final.csv', index = False)