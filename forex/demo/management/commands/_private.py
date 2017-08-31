import urllib3, time
from bs4 import BeautifulSoup
from demo.models import DataModel
from forex.settings import *


# This function is getting data from website as HTML and parsing it.
def get_data():
    http = urllib3.PoolManager()
    while True:
        response = http.request('GET', 'http://webrates.truefx.com/rates/connect.html?f=html&c=EUR/USD')
        html = response.data
        soup = BeautifulSoup(html, 'html.parser')
        list = [repr(string) for string in soup.strings]

        currency1 = list[0]
        print('Currency: {}'.format(currency1))

        timestamp = list[1]
        timestamp = (int(timestamp[1:-1]))
        print('Timestamp: {}'.format(timestamp))

        a = list[2]
        a = a[1:-1]
        sk = list[3]
        sk = str(sk[1:-1])
        ask = float(a + sk)
        print('Ask: {}'.format(ask))

        bi = list[4]
        bi = bi[1:-1]
        d = list[5]
        d = str(d[1:-1])
        bid = float(bi + d)
        print('Bid: {}'.format(bid))

        low = list[6]
        low = float(low[1:-1])
        print('Low: {}'.format(low))

        high = list[7]
        high = float(high[1:-1])
        print('High: {}'.format(high))

        open = list[8]
        open = float(open[1:-1])
        print('Open: {}'.format(open))

        new_data = {
            'currency': currency1,
            'timestamp': timestamp,
            'ask': ask,
            'bid': bid,
            'low': low,
            'high': high,
            'open': open
        }
        DataModel.objects.create(**new_data)
        time.sleep(60)
