import psycopg2

db_username = 'peddn'

print('Executing db_setup script.')

conn = psycopg2.connect('dbname=postgres')

cur = conn.cursor()

cur.execute('ALTER ROLE ' + db_username + ' SET client_encoding TO ' + "'utf8'" + ';')

cur.execute('SELECT * FROM pg_catalog.pg_roles')
for row in cur.fetchall():
    print('SELECT' + str(row))

cur.close()
conn.close()

print('Done.')
