from flask_mail import Mail, Message
#from flask import Flask

class My_Mail:
    def __init__(self, app):
        self.mail = Mail(app)

    def ab_send_mail(self, mail_addresses):
        msg = Message("[まちもりブザー]異常を検知しました", #title
                      sender="ac6328mats@g.kumamoto-nct.ac.jp", # 送信元
                      bcc=mail_addresses, # 送信先
                      charset="shift_jis") # 日本語表示するため
        msg.body = "異常を検知しました"
        self.mail.send(msg) #メール送信

    def bz_send_mail(self, mail_addresses):
        msg = Message("[まちもりブザー]ブザーが鳴らされました",
                      sender="ac6328mats@g.kumamoto-nct.ac.jp",
                      bcc=mail_addresses,
                      charset="shift_jis")
        msg.body = "ブザーが鳴らされました。\nもし誤操作だった場合は以下のリンクをクリックしてください\nhttp://machimori.japanwest.cloudapp.azure.com"
        self.mail.send(msg)

    def wio_get_mail(self, mail_addresses, method, lat, lon):
        msg = Message("[連絡用]Wioからデータがきました",
                      sender="ac6328mats@g.kumamoto-nct.ac.jp",
                      bcc=mail_addresses,
                      charset="shift_jis")
        msg.body = "Wioからデータがきました。\n" + method + "通信\nlat : " + str(lat) + "\nlon : " + str(lon)
        self.mail.send(msg)

if __name__ == "__main__":
    #app = Flask(__name__)
    #mail = My_Mail(app)
    #mail.ab_send_mail(['ac6328mats@g.kumamoto-nct.ac.jp', 'ac6292tsur@g.kumamoto-nct.ac.jp'])
    print('done')
