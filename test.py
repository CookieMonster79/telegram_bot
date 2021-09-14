import random

import psycopg2

con = psycopg2.connect(
    database="d80f0uj85llbhp",
    user="pspdigkdmeocay",
    password="20761c78ace93389b679235bfc5bf3878d2813e39ddf4ed1112b1a41241f787e",
    host="ec2-54-73-152-36.eu-west-1.compute.amazonaws.com",
    port="5432"
)

i = random.randint(1, 100)

cur = con.cursor()

cur.execute('SELECT * FROM public."Stickers" WHERE id = ' + str(i))

rows = cur.fetchall()

for row in rows:
    print(row[1])

con.close()