import psycopg2

db_username = 'peddn'

print('Executing db_setup script.')

conn = psycopg2.connect('dbname=postgres')

cur = conn.cursor()

result  = cur.execute('ALTER ROLE ' + db_username + ' SET client_encoding TO ' + "'utf8'" + ';')

print('RESULT: ' + result)

cur.close()
conn.close()

print('Done.')
