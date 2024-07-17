from tkinter import *
import re
import datetime
from datetime import date
from database import checkAppointment, setAppointment


def resetFlags():
    return {
        'isGreeted': 0,
        'isUKCitizen': 0,
        'Name':"",
        'dob':"",
        'isValidPassport': 0,
        'passportno': '',
        'isValidDate': 0,
        'date': "01/01/2022",
        'slots': [],
    }


Flags = resetFlags()


def get_response(message):
    UK_passport_regex = "[A-Z]{1}[0-9]{7}"  # 123456789
    global Flags
    if Flags['isGreeted'] == 0:
        if True in [(i in message.lower()) for i in ["hey", "hi", "hello", "good morning", "good afternoon", "good evening"]]:
            Flags['isGreeted'] = 1
            return "Hey There! Please tell us A few details to avail services \n Are you in UK?"
    else:
        if Flags['isUKCitizen'] == 0:
            if True in [(i in message.lower()) for i in ["yes", "y", "true", "yeah"]]:
                Flags['isUKCitizen'] = 1
                return "Please Enter Your Name"
            else:
                Flags = resetFlags()
                return "Sorry, book an appointment after coming to UK."
        else:
            if Flags['isUKCitizen'] == 1:
                if Flags['Name'] == "":
                    Flags['Name'] = message.strip()
                    return 'Please Enter Your DOB(dd/mm/yyyy)'
                else:
                    if Flags['dob'] == '':
                        Flags['dob'] = message.strip()
                        return "Please Enter Your Valid passport number"
                    else:
                        if Flags['isValidPassport'] == 0:
                            if re.match(UK_passport_regex, message.strip()):
                                Flags['isValidPassport'] = 1
                                Flags['passportno'] = message.strip()
                                return "Passport is valid! \nPlease Enter A Date for booking (dd/mm/yyyy):"
                            else:
                                return "Passport is Invalid!! Please Enter A Valid Passport number"
                        else:
                            if Flags['isValidDate'] == 0:
                                if not(checkDate(message.strip())):
                                    return "Please Enter A Valid Date (dd/mm/yyyy)"
                                Flags['date'] = message.strip()
                                Flags['slots'] = checkAppointment(Flags['date'])
                                if type(Flags['slots']) == type("asdfg"):
                                    return f"{Flags['slots']} please choose another date(dd/mm/yyyy)"
                                else:
                                    Flags['isValidDate'] = 1
                                    ret = f"Choose from the following for {Flags['date']}\n"
                                    for i, slot in enumerate(Flags['slots']):
                                        ret += f"[{i+1}] {slot} \n"
                                    ret += "\nNOTE: your appointment will be booked on the basis of your selection and the availablity"
                                    return ret
                            else:
                                status = setAppointment(
                                    Flags['passportno'], Flags['date'], Flags['slots'][int(message.strip())-1], Flags['Name'], Flags['dob'])
                                retStr = f"your booking for {Flags['date']}, \nslot of {Flags['slots'][int(message.strip())-1]} was {status}, \nThankyou for using our services! \n\nSee you soon."
                                Flags = resetFlags()
                                return retStr
            else:
                Flags = resetFlags()
                return "Sorry, book an appointment after coming to UK."
    return "How may I help you!"


def checkDate(datestring):
    today = date.today()
    curr = today.strftime("%d/%m/%Y").split('/')
    ref = datestring.split('/')
    d1 = datetime.datetime(int(curr[2]), int(curr[1]), int(curr[0]))
    d2 = datetime.datetime(int(ref[2]), int(ref[1]), int(ref[0]))
    if d1 < d2:
        return True
    return False


bot_name = "Alice(Bot)"
BG_BASE = "#285960"
BG_COLOR = "#8AA6AA"
TEXT_COLOR = "#000000"
# TEXT_COLOR = "#C2D1D3"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatBot:
    def __init__(self):
        self.main = Tk()
        self.setup_win()

    def run(self):
        self.main.mainloop()

    def setup_win(self):
        self.main.title("Chatbot")
        self.main.resizable(width=False, height=False)
        self.main.configure(width=590, height=570, bg=BG_COLOR)

        header = Label(self.main, bg="#2C3E50", fg='#FFFFFF', text="Welcome", font=FONT_BOLD, pady=10)
        header.place(relwidth=1)

        self.text_panel = Text(self.main, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.text_panel.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_panel.configure(cursor="arrow", state=DISABLED)

        scroll = Scrollbar(self.text_panel)
        scroll.place(relheight=1, relx=0.974)
        scroll.configure(command=self.text_panel.yview)

        footer = Label(self.main, bg=BG_BASE, height=80)
        footer.place(relwidth=1, rely=0.825)

        self.text_input = Entry(footer, bg="#FFFFFF", fg='#000000', font=FONT)
        self.text_input.place(
            relwidth=0.74, relheight=0.04, rely=0.015, relx=0.011)
        self.text_input.focus()
        self.text_input.bind("<Return>", self.send_on_enter)

        send = Button(footer, text="Send", font=FONT_BOLD, width=20, bg=BG_BASE, command=lambda: self.send_on_enter(None))
        send.place(relx=0.77, rely=0.015, relheight=0.04, relwidth=0.22)

    def send_on_enter(self, event):
        msg = self.text_input.get()
        self.append_message(msg, "You")

    def append_message(self, msg, sender):
        if not msg:
            return
        self.text_input.delete(0, END)

        msg1 = f"{sender}: {msg}\n\n"
        self.text_panel.configure(state=NORMAL)
        self.text_panel.insert(END, msg1)
        self.text_panel.configure(state=DISABLED)

        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_panel.configure(state=NORMAL)
        self.text_panel.insert(END, msg2)
        self.text_panel.configure(state=DISABLED)
        self.text_panel.see(END)


if __name__ == "__main__":
    gui = ChatBot()
    gui.append_message("Welcome to BRP appointment booking center",bot_name)
    gui.run()
