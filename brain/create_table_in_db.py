import sqlite3

connect = sqlite3.connect('all_data/all_things.db')
c = connect.cursor()
table_name = 'just_checking'
c.execute(f'''CREATE TABLE {table_name} (
            day Date,
            time time,            
            speech TEXT)
            ''')
connect.commit()
connect.close()
