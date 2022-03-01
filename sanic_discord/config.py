class Config:
    def __init__(self, secret, id, login_url, callback_url, redirect_url):
        self.secret = secret
        self.id = id
        self.login_url = login_url
        self.callback_url = callback_url
        self.redirect_url = redirect_url
