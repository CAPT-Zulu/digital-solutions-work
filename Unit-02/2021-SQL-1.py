import sqlite3

#connect to the database
con = sqlite3.connect("rockyconcrete.db")

#create a cursor/pointer to navigate the database
con.row_factory = sqlite3.Row #enables us to use column headings
cur = con.cursor() #is the pointer to use in the database

# sql = """
#         select *
#         from customers
#         where town = 'Brisbane';"""
#
# cur.execute(sql)
# results = cur.fetchall()
#
# print(results)

# Parameter Query
town_input = input("Enter the town to search for: ")
cr_limit_input = int(input("Enter the min for the cr_limit to search for: "))

sql = """
        select *
        from customers
        where town = ?
        and cr_limit >= ?"""

cur.execute(sql,(town_input,cr_limit_input,))
results = cur.fetchall()

if len(results) > 0:
    for row in results:
        print(row['cust_name'], 'lives in', row['street'], 'in', row['town'], 'cr limit is', row['cr_limit'])
else:
    print('No records found')