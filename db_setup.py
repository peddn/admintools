import sys
import psycopg2

db_name = sys.argv[1]
db_username = sys.argv[2]
db_password = sys.argv[3]

print('Executing db_setup script.')

conn = psycopg2.connect('dbname=postgres')
cur = conn.cursor()

cur.execute('CREATE DATABASE ' + db_name + ';')
cur.execute('CREATE USER ' + db_username + " WITH PASSWORD '" + db_password + "';")
cur.execute('ALTER ROLE ' + db_username + ' SET client_encoding TO ' + "'utf8'" + ';')
cur.execute('ALTER ROLE ' + db_username + ' SET default_transaction_isolation TO ' + "'read committed'" + ';')
cur.execute('ALTER ROLE ' + db_username + ' SET timezone TO ' + "'UTC'" + ';')
cur.execute('GRANT ALL PRIVILEGES ON DATABASE ' + db_name + ' TO ' + db_username + ';')

cur.execute('SELECT * FROM pg_catalog.pg_roles')
for row in cur.fetchall():
    print('SELECT' + str(row))

cur.close()
conn.close()

print('Done.')
