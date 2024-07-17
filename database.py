import sqlite3
def createDB():
    con = sqlite3.connect('appointmentsBooking') 
    cur = con.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS Appointments(
            passportNumber varchar(9),
            date varchar(9),
            slot varchar(7),
            CONSTRAINT pk_app Primary Key (date, slot)
            )
            ''')
                        
    con.commit()
    con.close()

slots=[
"8am-10am",
"11am-1pm",
"2pm-4pm",
"5pm-7pm"
]

def checkAppointment(datestring):
    con = sqlite3.connect('appointmentsBooking') 
    cur = con.cursor()
    rows = cur.execute(f'select slot from Appointments where date="{datestring.strip()}"')
    data = [i[0] for i in rows.fetchall()]
    con.close()
    ret = []
    # print(data)
    if len(data) == 4:
        return "no slots available"
    if len(data) >0 and len(data)<4:
        ret = slots.copy()
        for i in data:
            ret.pop(ret.index(i))
        # print(ret)
        return ret
    if len(data) ==0:
        return slots

def setAppointment(passport, datestring, slot):
    con = sqlite3.connect('appointmentsBooking') 
    cur = con.cursor()
    rows = cur.execute(f'insert into Appointments (passportNumber, date, slot) values ("{passport}", "{datestring}", "{slot}")')
    con.commit()
    con.close()
    return 'Successful'


# createDB()
# setAppointment('000000000', '10-09-2022', '8am-10am')
# setAppointment('000000000', '11-09-2022', '8am-10am')
# print(checkAppointment('10-09-2022'))
# print(checkAppointment('11-09-2022'))
