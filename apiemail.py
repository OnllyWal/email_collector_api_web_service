import imaplib
import email
import os

def acess(login, passw, status):

    '''Acessing the server and conecting with..'''
    objCon = imaplib.IMAP4_SSL("imap.gmail.com")
    objCon.login(login,passw)

    '''Where we want to acess: the Inbox page'''
    objCon.list()
    objCon.select('inbox', readonly = True)

    '''Return if were able to connect to gmail and email ids'''

    _, ids = objCon.search(None, status)

    return objCon, ids

def text(part, mail, subject):
    if part.get_payload(decode=True) != b'\r\n':
        if not os.path.exists(f'Texto/{mail}'):
            os.mkdir(f'Texto/{mail}')
        register = open(f'Texto/{mail}/{subject[0]}', 'wb')
        register.write(part.get_payload(decode=True))
        register.close
    else:
        pass

def attachment(part, mail, subject):
    if not os.path.exists(f'Fotos/{mail}'):
        os.mkdir(f'Fotos/{mail}')
    dir = open(f'Fotos/{mail}/{subject[0]}.jpg', 'wb')
    dir.write(part.get_payload(decode=True))
    dir.close()

def user_info(part):
    name = part['From'].split(" ")
    subject = part['Subject'].split(" ")
    char_remove = ['@', '.', '<', '>']
    for char in char_remove:
        mail = mail.replace(char, '_')
    return mail, subject
