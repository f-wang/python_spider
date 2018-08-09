import requests
from urllib.parse import urlencode
from pymongo import MongoClient
from multiprocessing.pool import Pool
import time


client = MongoClient('localhost', 27017)
db = client['tencent']
connection = db['tencent']

base_url = 'https://om.qq.com/VideoData/MediaVideoList?'

def get_page(page):
    params = {
        'startdate': '2018-08-03',
        'enddate': '2018-08-09',
        'limit': '8',
        'page': page,
        'fields': '2|3',
        'source': '0',
        'relogin': '1',
    }

    headers = {
        'cookie': 'pgv_pvid=4533940527; ts_uid=5529894900; tvfe_boss_uuid=f013f9f7eb708d71; pgv_pvi=2981295104; RK=cOZcDaHwbQ; ptcz=8422272e238fde7ce830e1f8f2557605f8751e10de30b574b000d1a84afb6b10; pac_uid=1_290868461; pt2gguin=o0290868461; o_cookie=290868461; luin=o0290868461; lskey=00010000a1eb83649dc4284da1c7612ac7973c4636be09759adbe05e6cefa00241e92193a3745048d6014973; main_login=qq; vuserid=203595375; vusession=dd589677909cbd8e67e575182478; encuin=596e6bea51f075a367d5bd9617482a49|290868461; lw_nick=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83|290868461|//thirdqq.qlogo.cn/g?b=sdk&k=mXoGzJA8XWvnfZN28k6F2A&s=40&t=1483306497|1; OM_EMAIL=13373649193; userid=5946998; ptui_loginuin=290868461; fname=JCPD; fimgurl=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_ls%2F0%2F2239988073_200200%2F0; rmod=1; omtoken=1e35ee7199; omtoken_expire=1533810189; uid=701027768; alertclicked=%7C1%7C; pgv_info=ssid=s5982862964; ts_last=om.qq.com/article/videoStatistic; TSID=jf5i31u82gto2gabidrucfk3m6; 9e67236d07bdc7152e6e2b42b7f00f43=22b1b69e3f1bcd86f640511ce25d3169def213eaa%253A4%253A%257Bi%253A0%253Bi%253A5946998%253Bi%253A1%253Bs%253A16%253A%2522290868461%2540qq.com%2522%253Bi%253A2%253Bi%253A43200%253Bi%253A3%253Ba%253A15%253A%257Bs%253A6%253A%2522status%2522%253Bi%253A2%253Bs%253A5%253A%2522phone%2522%253Bs%253A11%253A%252213373649193%2522%253Bs%253A2%253A%2522id%2522%253Bi%253A5946998%253Bs%253A9%253A%2522logintype%2522%253Bi%253A2%253Bs%253A5%253A%2522email%2522%253Bs%253A16%253A%2522290868461%2540qq.com%2522%253Bs%253A3%253A%2522uin%2522%253BN%253Bs%253A4%253A%2522wxid%2522%253BN%253Bs%253A6%253A%2522imgurl%2522%253Bs%253A55%253A%2522http%253A%252F%252Finews.gtimg.com%252Fnewsapp_ls%252F0%252F2239988073_200200%252F0%2522%253Bs%253A4%253A%2522name%2522%253Bs%253A4%253A%2522JCPD%2522%253Bs%253A10%253A%2522isVerified%2522%253Bb%253A1%253Bs%253A10%253A%2522isRejected%2522%253Bb%253A0%253Bs%253A9%253A%2522agreeAcpt%2522%253Bb%253A0%253Bs%253A6%253A%2522pwdChg%2522%253Bb%253A0%253Bs%253A9%253A%2522avatarChg%2522%253Bb%253A0%253Bs%253A2%253A%2522lk%2522%253Bs%253A24%253A%2522l0a9NsUwok0_ieJTY3gv_Q00%2522%253B%257D%257D'
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None


def get_video(json):
    data = json.get('data').get('list')
    if data:
        for item in data:
            yield {
                'videoTitle': item.get('title'),
                'videoUrl': item.get('url')
            }



def save_video_url(item):
    if connection.insert(item):
        print(item)


def main(page):
    json = get_page(page)
    for item in get_video(json):
        save_video_url(item)

GROUPS_START = 2
GROUPS_END = 86

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 1 for x in range(GROUPS_START, GROUPS_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()