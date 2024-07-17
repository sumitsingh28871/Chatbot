import sqlite3
conn = sqlite3.connect('appointmentsBooking') 
c = conn.cursor()
rows = c.execute('''
        select * from Appointments
        ''')
for row in rows:
    print(row)    
conn.close()