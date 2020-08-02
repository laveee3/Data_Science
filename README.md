# Data_Science
Data comparison against huge database and update the information using pandas and data science logic

Problem:
Oracle database - has millions of records of the people who belong and who belonged to the Institutions. 
Various details of the people are there. This work revolves around the contact information like email, phone and address.
Many a times we get large csv files with current details of people. The csv files would have records between 1000 to 500000.
This means each record in the csv file need to be verified against the database. And if any of the phone/email/address contact information between the csv file and database does not match, the info in the csv file needs to be entered into the database. 
For every record there is an unique identifier- EID

Solution:
Software used: Python 3.6, Anaconda, Jupiter Notes
Libraries used: numpy, panda, matplotlib, fuzzywuzzy, cx_Oracle
The programs step by step procedure:
1.	The csv file with which we have to refer the database is inputted.
2.	The csv input data is passed to the panda dataframe and needed columns are retained, duplicate rows and empty Eid rows are removed.
3.	The EID of all the records alone are fed to a list variable.
4.	Database connection is being established and using sql query a relevant table is accessed. The needed columns for all the EID in the csv file is extracted.
5.	This is being fed to another dataframe.
6.	Now we have the dataframe from csv file and dataframe from database for the same EID.
7.	For record in database, there maybe one or more phone numbers, email address, address (home or office or both).
The comparison starts now.

For email address:
8.	Each email address in csv file is compared one or more email address present in the database for the relevant EID. This is a string comparison.
Csv Email address that is not present in the database is added to a email_dataframe. These emails will be updated in the database later.

For phone number:
9.	Data unification/cleaning for the phone numbers present in both database and csv is done. Phone numbers comes in different format, it could be continuous number or it could brackets around area code or ‘-‘ between area codes and rest of the numbers.
10.	Each phone address in csv file is compared one or more phone address present in the database for the relevant EID. 
Csv Phone address that is not present in the database is added to a phone_dataframe. These phones will be updated in the database later.
For physical address comparison:
Logic 1:
if the number of lines matching EID is more than 1, create a df to put those many rows, "rows" while rows >0 and 
 break the loop if the addr comparison for that loop yields token_set_ratio > 83
If zipcode differs, state or city or house inside same city might be different
If zipcode is same, compare address line 1 and line 2
if zipcode is not given, compare city or state before address comparison

Logic2:	
11.	Fuzzywuzzy tool is so helpful. Of the many tokens (like partial token, token sort ratio), token set ratio perfectly fits the need. This helped to find the matching address and keep adding to the addr_dataframe with records with new address that is not in the database. Logic 2 is very light, easy and fast than the logic 1.
12.	Matplotlib is used to show how many records have new address from the total csv records.
13.	All the dataframes that has new phone/email/address are merged.
