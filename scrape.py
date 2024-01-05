import requests
import sys
from bs4 import BeautifulSoup
from flask import Flask, json

## http://127.0.0.1:5000/skrapster/mail/www.pod7kilo.cz

api = Flask(__name__)

@api.route('/skrapster/<par1>/<par2>', methods=['GET'])

def get_scrape(par1, par2):
    try:
        if par1 == 'mail':
            return functions.mail_scrape(par2)
    except requests.exceptions.ConnectionError:
        return 'Website not found'

class functions:
    def mail_scrape(par2):
        par2 = str('https://' + par2)
        print(par2)
        req = requests.get(par2)
      
        data = BeautifulSoup(req.text, 'html.parser')

        for li in data.find_all("p"):
            ppp = str(li.decode_contents().split('\n'))
            if 'email' in ppp:
                mail = ppp.split('#')[1].split('"')[0]
                de = ""
                k = int(mail[:2], 16)

                for i in range(2, len(mail)-1, 2):
                    de += chr(int(mail[i:i+2], 16)^k)
                mail = de

            elif '@' in ppp:
                try:
                    mail = ppp.split('mailto:')[1].split('"')[0]
                except:
                    continue
        print(mail)

        return str(mail)


if __name__ == '__main__':
    api.run()

