#! python3
# download4chan

import os,sys,bs4,requests
from pathlib import Path as p

def downloader(url,folderName=''):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    imgElems = soup.select(r".fileThumb")
    for i in range(len(imgElems)):
        try:
            imgUrl ='https:' + imgElems[i].get('href')
            print(os.path.basename(imgUrl))
            res = requests.get(imgUrl)
            res.raise_for_status()
            if i == 0 and folderName == '':
                os.makedirs(p(os.path.basename(imgUrl)), exist_ok=True)
                os.chdir(p(os.path.basename(imgUrl)))
                imageFile = open(p('./'+os.path.basename(imgUrl)),'wb')
            elif i == 0 and folderName:
                os.makedirs(p(folderName), exist_ok=True)
                os.chdir(p(folderName))
                imageFile = open(p('./'+os.path.basename(imgUrl)),'wb')
            else:
                imageFile = open(p('./'+os.path.basename(imgUrl)),'wb')
            for chunk in res.iter_content(1000000):
                imageFile.write(chunk)
            imageFile.close()
        except TypeError:
            continue

os.makedirs(p('4chan'),exist_ok=True)
os.chdir(p('4chan'))
if len(sys.argv) == 3:
    downloader(sys.argv[1],sys.argv[2])
elif len(sys.argv) == 2:
    downloader(sys.argv[1])
elif len(sys.argv) == 1:
    print('Usage: py download4chan.py {link}')
else:
    url = input('Enter a 4chan thread URL: ')
    downloader(url)
