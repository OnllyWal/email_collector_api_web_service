import imaplib
import email

def acess(login, passw):

    '''Acessing the server and conecting with..'''
    objCon = imaplib.IMAP4_SSL("imap.gmail.com")
    objCon.login(login,passw)

    '''Where we want to acess: the Inbox page'''
    objCon.list()
    objCon.select('inbox', readonly = True)

    '''Return if were able to connect to gmail and email ids'''

    _, ids = objCon.search(None, 'ALL')

    return objCon, ids

def text(part, nome):
    if part.get_payload(decode=True) != b'\r\n':
        register = open(f'Cadastro/{nome[0]}', 'wb')
        register.write(part.get_payload(decode=True))
        register.close
    else:
        pass

def attachment(part):
    filename = part.get_filename()
    dir = open(f'Fotos/{filename}', 'wb')
    dir.write(part.get_payload(decode=True))
    dir.close()