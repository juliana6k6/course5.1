from configparser import ConfigParser
# import psycopg2

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    print(dir(parser))
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
# def connect():
#     conn = None
#     try:
#         parser = ConfigParser()
#         parser.read('database.ini')
#
#         params = dict(parser.items('postgresql'))
#         print('Connecting to the PostgreSQL database...')
#         conn = psycopg2.connect(**params)
#         cur = conn.cursor()
#         cur.execute('SELECT version()')
#         db_version = cur.fetchone()
#         print(f'PostgreSQL database version: {db_version}')
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')


A = config()
print(A)
