class Email:
    def __init__(self, sender_name: str, complete_name: str, email_name: str, body: str, attachments: list):
        """Inicializa o objeto Email com os parâmetros fornecidos."""
        self.sender_name = sender_name
        self.complete_name = complete_name
        self.email_name = email_name
        self.body = body
        self.attachments = attachments

    def __repr__(self):
        """Representação textual do objeto Email."""
        return (f"Email(sender_name={self.sender_name}, complete_name={self.complete_name}, "
                f"email_name={self.email_name}, body={self.body[:30]}..., "
                f"attachments={len(self.attachments)} attachments)")
        

class Direct_Email(Email):
    def __init__(self, sender_name: str, complete_name: str, email_name: str, body: str, attachments: list, subject: str):
        """Inicializa o objeto Direct_Email, que herda de Email."""
        super().__init__(sender_name, complete_name, email_name, body, attachments)
        self.subject = subject

    def __repr__(self):
        """Representação textual do objeto Direct_Email."""
        return (f"Direct_Email(sender_name={self.sender_name}, complete_name={self.complete_name}, "
                f"email_name={self.email_name}, subject={self.subject}, "
                f"attachments={len(self.attachments)} attachments)")


class Forwarded_Email(Email):
    def __init__(self, sender_name: str, complete_name: str, email_name: str, body: str, attachments: list, subject: str, origin_name: str, origin_address: str):
        """Inicializa o objeto Forwarded_Email, que herda de Email."""
        super().__init__(sender_name, complete_name, email_name, body, attachments)
        self.subject = subject
        self.origin_name = origin_name
        self.origin_address = origin_address

    def __repr__(self):
        """Representação textual do objeto Forwarded_Email."""
        return (f"Forwarded_Email(sender_name={self.sender_name}, complete_name={self.complete_name}, "
                f"email_name={self.email_name}, subject={self.subject}, "
                f"origin_name={self.origin_name}, origin_address={self.origin_address}, "
                f"attachments={len(self.attachments)} attachments)")
