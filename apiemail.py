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
    '''Some emails have "empty" text parts, so here we gonna remove then'''
    if part.get_payload(decode=True) != b'\r\n':

        '''Create a folder with the sender email'''
        if not os.path.exists(f'Texto/{mail}'):
            os.mkdir(f'Texto/{mail}')

        '''Save the text on a file with the email subject'''
        register = open(f'Texto/{mail}/{subject[0]}', 'wb')
        register.write(part.get_payload(decode=True))
        register.close
    else:
        pass

def attachment(part, mail, subject):

    '''Create a folder with the sender email'''
    if not os.path.exists(f'Fotos/{mail}'):
        os.mkdir(f'Fotos/{mail}')

    '''Save attachment on a file with the email subject'''    
    dir = open(f'Fotos/{mail}/{subject[0]}.jpg', 'wb')
    dir.write(part.get_payload(decode=True))
    dir.close()

def user_info(part):

    '''The OS can't make a directory with some characters, so here we replace these chars...'''
    name = part['From'].split(" ")
    subject = part['Subject'].split(" ")
    mail = name[-1]
    char_remove = ['@', '.', '<', '>']
    for char in char_remove:
        mail = mail.replace(char, '_')
    return mail, subject
