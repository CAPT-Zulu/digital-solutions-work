import sqlite3
#connect to the database
con = sqlite3.connect("people.db")

#create a cursor/pointer to navigate the database
con.row_factory = sqlite3.Row #enables us to use column headings
cur = con.cursor() #is the pointer to use in the database

x = 1
while (x):
    name_valid = 0
    age_valid = 0

    print('Adding a new person to the database input:')

    while (name_valid==0):
        name = input("Enter your name (Required): ")
        if len(name) > 1:
            name_valid = 1

    while (age_valid==0):
        age = int(input("Enter your age (Required): "))
        if age > 18 and age < 255:
            age_valid = 1

    sex = input("Enter the sex you identify as (Optional): ")

    if len(sex) < 3:
        sex = "Rather not say"

    earns = int(input("Enter your earnings (Required): "))

    likes = input("Enter something you like (Optional): ")

    dislikes = input("Enter something you dislike (Optional): ")

    sql = """
            insert
            into members (name, age, sex, earns, likes, dislikes)
            values (?, ?, ?, ?, ?, ?);"""
    cur.execute(sql, (name, age, sex, earns, likes, dislikes),)

    con.commit()

    if (cur.rowcount):
        print(name, 'was successfully added to the database')
        x = 0
    else:
        print('An error occured when adding:', name, 'to the database')