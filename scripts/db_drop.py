import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import DuplicateDatabase, DuplicateObject

project = sys.argv[1]

print('Executing db_setup script.')

# this script assumes that it runs as postgres unix user
# connect to the 'postgres' standard database
con = psycopg2.connect('dbname=postgres')


con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()


cur.execute('DROP DATABASE ' + project + ';')

cur.execute('DROP USER ' + project + ';')


cur.close()
con.close()

print('Done.')
