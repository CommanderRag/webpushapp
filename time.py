episode_number1 = open('number.txt' , 'r')
episode_number = episode_number1.readlines()
print(episode_number)
import os
import re
import sys
import requests
import json
'''
headers_send = {
    'Content-Type': 'application/json',
}
'''
from bs4 import BeautifulSoup

print("working")

url = "https://4anime.to/boruto-naruto-next-generations-episode-{}".format(episode_number)
r = requests.get(url)
html = r.content
soup = BeautifulSoup(html, 'html.parser')
text = soup.find_all(text=True)
output = ""
blacklist = [
    '[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script'
            ]
for t in text:
    if t.parent.name not in blacklist:
        output += '{}'.format(t)

import json
if(output.find("Episode {}".format(episode_number)))==-1:
    
    
    data = '{"number":"number1"}'.replace("number1",str(episode_number))

    response = requests.post('https://mywebpushapp.herokuapp.com/false', data=data)
    print(response.status_code)
    
    write_r = open('exec_number.txt','r')
    if(write_r.readlines() == '0'):
      exec_num = write_r.readlines()
      exec_num = int(exec_num)
      exec_num = exec_num + 1
      write_w = open('exec_number.txt', 'w+')
      write_w.write(str(exec_num))
      write_w.close()
    elif(write_r.readlines() == '22' or '23'):
          data = '{"number":"number1"}'.replace("number1","null")
          response = requests.post('https://mywebpushapp.herokuapp.com/false', data=data)
          print(response.status_code)
          

else:
    
    data = '{"number":"number1"}'.replace("number1",str(episode_number))

    response = requests.post('https://mywebpushapp.herokuapp.com/true', data=data)
    print(response.status_code)

    write_r = open('exec_number.txt', 'r')
    if(write_r.readlines() == '22' or '23'):
        write_w = open('exec_number.txt' , 'w+')
        write_w.write('0')
        write_w.close()
        write_ep_r = open('number.txt', 'r')
        episode_num = write_ep_r.readlines()
        episode_num = int(episode_num)
        episode_num = episode_num + 1
        write_ep_r.close()
        write_ep_w = open('number.txt' ,'w+')
        write_ep_w.write(episode_num)
        write_ep_w.close()