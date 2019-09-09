# coding: UTF-8
import json
from datetime import date, datetime
from DB import DB
import requests

def iktoaddress(lat, lon):
    url = "https://www.finds.jp/ws/rgeocode.php?json&lat="+str(lat)+"&lon="+str(lon)
    response = requests.get(url)
    js = json.loads(response.text)
    ans = js['result']['prefecture']['pname']+js['result']['municipality']['mname']+js['result']['local'][0]['section']+js['result']['local'][0]['homenumber']
    return ans

class My_Json():
    def data_molding(self, okind, odata, skind, sdata):
        db = DB()
        plot_list = []
        for olis in odata:
            if olis[4] == 1:
                continue
            plot_dict = {}
            plot_dict['kind'] = okind
            plot_dict['lat'] = olis[1]
            plot_dict['lon'] = olis[2]
            plot_dict['time'] = olis[3].strftime('%Y/%m/%d %H:%M:%S')
            plot_dict['case'] = olis[5]
            plot_dict['buzzer_num'] = olis[0]
            plot_dict['address'] = iktoaddress(olis[1], olis[2])
            plot_list.append(plot_dict)

        for slis in sdata:
            plot_dict = {}
            plot_dict['kind'] = skind
            plot_dict['lat'] = slis[2]
            plot_dict['lon'] = slis[3]
            plot_dict['name'] = slis[4]
            plot_dict['address'] = slis[1]
            #plt_dict['img']
            plot_list.append(plot_dict)
        return plot_list

if __name__ == '__main__':
    i_json = My_Json()
    #i_json.data_molding()
