import ssl
import nude
import requests
import urllib.request
import pymysql
import time
import shutil
from nude import Nude
from bs4 import BeautifulSoup

fix_link = "http://gall.dcinside.com"
upload_dir = './store/'

url = 'http://gall.dcinside.com/board/lists/?id=baseball_new6&page=1'
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'ko-KR,ko;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Host': 'gall.dcinside.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}

r = requests.get(url, headers=headers)
html = r.text
soup = BeautifulSoup(html, "lxml")
rows = soup.find_all("tr", { "class" : "us-post" })

#print('rows -> ', rows)

for row in rows:
    #print(row)
    gall_num = row.find("td", {"class":"gall_num"}).string
    gall_tit = row.find("td", {"class":"gall_tit"}).text.strip().replace('\n',' ')
    gall_link = fix_link + row.a.get('href')
    gall_img_check = row.find("td", {"class":"gall_tit"}).find("em", {"class":"icon_pic"})

    if gall_img_check == None:
        print("pass")
        print('========================================')
        continue

    print('gall_num -> ', gall_num)
    print('gall_tit -> ', gall_tit)
    print('gall_link -> ', gall_link)
    print('-----------------------------')


    r = requests.get(gall_link, headers=headers)
    inner_html = r.text
    soup = BeautifulSoup(inner_html, "lxml")
    files = soup.find_all("ul", { "class" : "appending_file" })
    for file in files:
        cnt = 0
        for n in file.find_all('li'):

            pure_file_name = n.a.string
            pure_file_link = n.a.get('href')

            tmp_a = "https://image.dcinside.com/download.php"
            tmp_b = "https://dcimg3.dcinside.co.kr/viewimage.php"
            pure_file_link = pure_file_link.replace(tmp_a, tmp_b)

            print('pure_file_name -> ', pure_file_name)
            print('pure_file_link -> ', pure_file_link)

            img_file = urllib.request.urlopen(pure_file_link, context=ssl.SSLContext())
            full_dir = upload_dir + gall_num + '#' + str(cnt) + ".png"
            full_path = gall_num + '#' + str(cnt) + ".png"

            print("full_dir -> ", full_dir)
            print("full_path -> ", full_path)

            f = open(full_dir, 'wb')
            f.write(img_file.read())
            f.close()

            #time.sleep(1)

            print(nude.is_nude(full_dir))

            n = Nude(full_dir)
            n.parse()
            if nude.is_nude(full_dir) == True:
                shutil.move(full_dir, './adult/' + full_path)
            print("damita :", n.result, n.inspect())

            cnt += 1

            print('---------------------------------------')
        print('========================================')
