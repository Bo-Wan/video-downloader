import sys
import requests
import json
import re

baseUrl = 'https://player.vimeo.com/video/'


with open("targets.txt") as f:
    lines = f.readlines()
    for line in lines:
        vid = line.rstrip()
        url = baseUrl + vid

        # response = requests.get(url)
        response = requests.get(url, headers = {"Referer":"https://www.budovideos.com/"})
        m = re.search(r'(?<=<title>)([\s\S]*?)(?=</title>)', response.text)
        if m:
           print('\nVideo [' + vid + ']: <' + m.group() + '>\n')
           # m = re.search(r'(?<={var\ r=)([\s\S]*?)(?=;if)', response.text)
           # if m:
           #     j = json.loads(m.group())
           #     for link in j['request']['files']['progressive']:
           #         print(link['quality'] + ' download link:\n' + link['url'] + '\n')
           # else:
           #     print("ERROR: No download link found for video " + vid)
        else:
           print("ERROR: No title found for video " + vid)

        print('\n')
