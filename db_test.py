import psycopg2

db_name = 'peddn'
db_username = 'peddn'

conn = psycopg2.connect('dbname=' + db_name + ' user=' + db_username)

cur = conn.cursor()

cur.execute('ALTER ROLE ' + db_username + ' SET client_encoding TO ' + "'utf8'" + ';')

cur.close()
conn.close()

