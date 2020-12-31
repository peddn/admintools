import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import InvalidCatalogName, UndefinedObject

project = sys.argv[1]

print('[INFO] Executing db_drop script.')

# this script assumes that it runs as postgres unix user
# connect to the 'postgres' standard database
con = psycopg2.connect('dbname=postgres')


con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

try:
    print('\t[INFO] Dropping database "' + project + '"')
    cur.execute('DROP DATABASE ' + project + ';')
except InvalidCatalogName as error:
    print('\t[ERROR] ' + str(error).strip())
else:
    print('\t[INFO] Done')

try:
    print('\t[INFO] Dropping user "' + project + '"')
    cur.execute('DROP USER ' + project + ';')
except UndefinedObject as error:
    print('\t[ERROR] ' + str(error).strip())
else:
    print('\t[INFO] Done')

cur.close()
con.close()

print('[INFO] Done')
