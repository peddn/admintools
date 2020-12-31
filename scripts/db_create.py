import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import DuplicateDatabase, DuplicateObject

project = sys.argv[1]
db_password = sys.argv[2]

print('Executing db_setup script.')

# this script assumes that it runs as postgres unix user
# connect to the 'postgres' standard database
con = psycopg2.connect('dbname=postgres')


con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

try:
    cur.execute('CREATE DATABASE ' + project + ';')
except DuplicateDatabase as error:
    print('ERROR: ' + error)

try:
    cur.execute('CREATE USER ' + project + " WITH PASSWORD '" + db_password + "';")
except DuplicateObject as error:
    print('ERROR: ' + error)
else:
    cur.execute('ALTER ROLE ' + project + ' SET client_encoding TO ' + "'utf8'" + ';')
    cur.execute('ALTER ROLE ' + project + ' SET default_transaction_isolation TO ' + "'read committed'" + ';')
    cur.execute('ALTER ROLE ' + project + ' SET timezone TO ' + "'UTC'" + ';')
    cur.execute('GRANT ALL PRIVILEGES ON DATABASE ' + project + ' TO ' + project + ';')

cur.execute('SELECT * FROM pg_catalog.pg_roles')
for row in cur.fetchall():
    if str(row).startswith(project):
        print(str(row))

cur.close()
con.close()

print('Done.')
