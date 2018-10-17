import pymysql
from urllib.request import urlretrieve
import requests
import json
import re
import string

########################################################################################################
# 2422文件，一个一个文件下载
# • 控制进度，用vid加extra column,下载完没有
#     vdata_download
#     alter table target add column dl_stat BOOL;
#     1 = downloaded + succeeded; 0 = download started but not succeeded; NULL == not downloaded
#     select * from target order by vid desc limit 1;
#
#     下一个应该下载的文件
#     select * from target where dl_stat is NULL or dl_stat = 0 order by vid desc limit 1;
#
#     定义文件名规则
#
# • 人工/脚本自动每次从数据库检查，先处理最新的vid，然后往老的处理。下载成功 = true 的跳过不处理，false和null的开干
# • 用get-vid-details拿到下载链接, urllib下载
# • 用ffmpeg检查下载成功与否，失败则重复
# • 下载下一个文件
########################################################################################################

def getDownloadLink(vendor, vid):
    url = 'https://player.vimeo.com/video/' + vid

    if vendor == 'BJJ Fanatics':
        response = requests.get(url)
    elif vendor == 'BudoVideos':
        response = requests.get(url, headers = {"Referer":"https://www.budovideos.com/"})
    else:
        print('Wrong vendor type: ' + vendor + ". Exitting...")
        exit(0)

    m = re.search(r'(?<=<title>)([\s\S]*?)(?=</title>)', response.text)
    if m:
       print("\nVideo: <" + m.group() + ' @ ', end='')
       # m = re.search(r'(?<={var\ r=)([\s\S]*?)(?=;if)', response.text)
       m = re.search(r'(?<=var\ config\ =\ )([\s\S]*?)(?=;)', response.text)
       if m:
           # print("Json = " + m.group())
           j = json.loads(m.group())
           # print(j['request']['files']['progressive'])
           max = 0
           for link in j['request']['files']['progressive']:
               if link['width'] > max:
                   max = link['width']
               # print(link['quality'] + ' download link:\n' + link['url'] + '\n')
           for link in j['request']['files']['progressive']:
               if link['width'] == max:
                   print(link['quality'] + '\n' + link['url'] + '\n')
                   return link['url']
           print('Error: No downloading link found, exiting...')
           exit(0)

       else:
           print("ERROR: No download link found for video " + vid)
           print(response.text)
           exit(0)

    else:
       print("ERROR: No title found for video " + vid)
       exit(0)


# Get Mariadb cursor
#conn = pymysql.connect(host='localhost', user='root', password='9ksASd0-123!', database='vdata_download', autocommit=True)
conn = pymysql.connect(host='localhost', user='root', database='vdata_download', autocommit=True)
cursor = conn.cursor()

defaultDest = '/media/sf_shared/vdata-download'
BJJFDest = '/media/sf_shared/vdata-download/BJJFanatics/'
BudoDest = '/media/sf_shared/vdata-download/BudoVideos/'
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

while(True):

    print('Querying new download target...')
    # Get download target
    query = 'select * from target where dl_stat is NULL or dl_stat = 0 order by vid desc limit 1;'
    # query = "select * from target where vid = 284022699 order by vid desc limit 1;"
    cursor.execute(query)
    result = cursor.fetchall()

    if len(result) is 0:
        print('Download finished.')
        exit(0)

    target = result[0]

    vid = target[1]
    title = target[2]
    vendor = target[3]
    stat = target[4]

    # Saving Destination
    savingDest = defaultDest;
    if vendor == 'BJJ Fanatics':
        print('Vid = [' + str(vid) + ']\nVendor = [BJJ Fanatics]')
        savingDest = BJJFDest

    elif vendor == 'BudoVideos':
        print('Vid = [' + str(vid) + ']\nVendor = [BudoVideos]')
        savingDest = BudoDest;

    else:
        print('Fatal error: vid ' + vid + ' vendor type not recognised')
        exit(0)

    print('Saving destination: [' + savingDest + ']')

    # File name
    rawFileName = str(vid) + ' ' + title + '.mp4'
    fileName = ''.join(c for c in rawFileName if c in valid_chars)
    print('New file name: [' + fileName + ']')
    print('Final target destination: [' + savingDest + fileName + ']')

    # Get url
    print('Getting url...')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    downloadUrl = getDownloadLink(vendor, str(vid))
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ')
    print('Downloading url get: ' + downloadUrl)

    # Download
    print('Starting download...')
    urlretrieve (downloadUrl, savingDest + fileName)
    print('Downloading Done!')

    # DB update
    print('Updating database...')
    query = "update target set dl_stat = 1 where vid = " + str(vid) + ";"
    print("exec: " + query)
    cursor.execute(query)
    print('Database updated!')
