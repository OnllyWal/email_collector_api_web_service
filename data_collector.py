import imaplib
import email


def email_reader():
    
    ''' Here you have to insert the email and the 16 characters password, avalaible by Google Account (Security Page)'''
    login = "donarosadata@gmail.com"
    passw = "dmrs nqbs hmvq otpg"

    '''Acessing the server and conecting with..'''
    objCon = imaplib.IMAP4_SSL("imap.gmail.com")
    conection = objCon.login(login,passw)

    '''Where we want to acess: the Inbox page'''
    objCon.list()
    objCon.select('inbox', readonly = True)

    '''Return if were able to connect to gmail and email ids'''

    answers, ids = objCon.search(None, 'ALL')

    '''looping the gmail inbox, entering each id'''
    for num in ids[0].split():
        results, data = objCon.fetch(num, '(RFC822)')
        text = data[0][1]
        text = text.decode('utf-8')
        text = email.message_from_string(text)

        '''getting into the email part's'''
        for part in text.walk():

            '''Detecting who send the message'''
            if part['From'] !=  None:
                nome = part['From'].split(" ")
            
            '''if is a text (register phase)'''
            if part.get_content_maintype() == 'text' and part.get_content_type() == 'text/plain':
                if part.get_payload(decode=True) == b'\r\n':
                    continue
                register = open(f'Cadastro/{nome[0]}', 'wb')
                register.write(part.get_payload(decode=True))
                register.close

            '''if is a attachment (photos sharing)'''
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            dir = open(f'Fotos/{filename}', 'wb')
            dir.write(part.get_payload(decode=True))
            dir.close()
            return True
