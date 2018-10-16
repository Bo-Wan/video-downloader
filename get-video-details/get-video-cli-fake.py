import sys
import requests
import json
import re

vid = sys.argv[1]
url = 'https://player.vimeo.com/video/' + vid

response = requests.get(url, headers = {"Referer":"https://www.budovideos.com/"})
m = re.search(r'(?<=<title>)([\s\S]*?)(?=</title>)', response.text)
if m:
   print("\nVideo: <" + m.group() + '>\n')
   m = re.search(r'(?<={var\ r=)([\s\S]*?)(?=;if)', response.text)
   if m:
       # print("Json = " + m.group())
       j = json.loads(m.group())
       # print(j['request']['files']['progressive'])
       for link in j['request']['files']['progressive']:
           print(link['quality'] + ' download link:\n' + link['url'] + '\n')

   else:
       print("ERROR: No download link found for video " + vid)
else:
   print("ERROR: No title found for video " + vid)
