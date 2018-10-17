import sys
import requests
import json
import re

vid = sys.argv[1]
url = 'https://player.vimeo.com/video/' + vid

response = requests.get(url)
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

   else:
       print("ERROR: No download link found for video " + vid)
       print(response.text)

else:
   print("ERROR: No title found for video " + vid)
