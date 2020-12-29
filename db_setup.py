import psycopg2

db_username = 'peddn'

conn = psycopg2.connect('dbname=postgres')

cur = conn.cursor()

result  = cur.execute('ALTER ROLE ' + db_username + ' SET client_encoding TO ' + "'utf8'" + ';')

print(result)

cur.close()
conn.close()
