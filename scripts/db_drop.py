import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import InvalidCatalogName, UndefinedObject

project = sys.argv[1]

print('Executing db_setup script.')

# this script assumes that it runs as postgres unix user
# connect to the 'postgres' standard database
con = psycopg2.connect('dbname=postgres')


con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

try:
    cur.execute('DROP DATABASE ' + project + ';')
except InvalidCatalogName as error:
    print('ERROR: ' + str(error))

try:
    cur.execute('DROP USER ' + project + ';')
except UndefinedObject as error:
    print('ERROR: ' + str(error))

cur.close()
con.close()

print('Done.')
