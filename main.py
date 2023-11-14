from apiemail import acess, text, attachment
import email
import imaplib

login = "donarosadata@gmail.com"
passw = "dmrs nqbs hmvq otpg"

objCon, ids = acess(login, passw)

for num in ids[0].split():
    results, data = objCon.fetch(num, '(RFC822)')
    content = data[0][1]
    content = content.decode('utf-8')
    content = email.message_from_string(content)

    '''getting into the email part's'''
    for part in content.walk():

        '''Detecting who send the message'''
        if part['From'] !=  None:
            nome = part['From'].split(" ")
        if part.get_content_maintype() == 'text' and part.get_content_type() == 'text/plain':
            text(part, nome)
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            attachment(part)