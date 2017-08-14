#!/usr/bin/python3

import requests
import re
from bs4 import BeautifulSoup

CLASS_LIST = ["druid", "hunter", "mage", "paladin", "priest", "rogue", "shaman", "warlock", "warrior"]
CLASS_LIST_KO = ["드루이드", "사냥꾼", "마법사", "성기사", "사제", "도적", "주술사", "흑마법사", "전사"]

if __name__ == '__main__':
    print('데이터를 받아옵니다...')
    req = requests.get('http://www.heartharena.com/ko/tierlist')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    
    new_tags = soup.find_all("span", string=re.compile(r"신규"))
    for t in new_tags:
        t.decompose()

    print('직업을 선택하세요 (', end='')
    for i, c in enumerate(CLASS_LIST_KO, 1):
        print('{0}.{1}'.format(i, c), end=' ')
    print('\b):', end=' ')

    selection = input()
    selection = int(selection)
    if selection < 1 or selection > len(CLASS_LIST):
        print('잘못된 입력입니다.')

    tier_data = soup.find('section', class_=CLASS_LIST[selection-1])
    if tier_data != None:
        print(r"'{0}'를 선택했습니다.".format(CLASS_LIST_KO[selection-1]))
        while True:
            cname = input('카드 이름을 입력하세요 : ')

            if cname == 'exit':
                break

            names = cname.split()
            for i, n in enumerate(names):
                if i == 0:
                    print('-----------------------------------')

                find_text = re.sub('(.)', r'\1.*', n)
                find_text = "\\b" + find_text
                card_list = tier_data.find_all('dt', string=re.compile(find_text))
                if len(card_list) == 0:
                    print("카드를 찾을 수 없습니다.")
                    print('-----------------------------------')
                    continue

                for cdata in card_list:
                    score = cdata.find_next_sibling('dd')
                    tier_obj = cdata.find_parent('li', class_='tier')
                    tier = tier_obj.find('header')
                    
                    suited = ""
                    if len(cdata['class']) > 2:
                        suited = " - 이 직업에 "
                        if cdata['class'][2] == "higher":
                            suited += "더 좋음"
                        else:
                            suited += "더 나쁨"

                    print('{0} ({1} {2})'.format(cdata.text.strip(),
                        score.text.strip(), tier.text.strip()), end='')
                    print(suited)

                print('-----------------------------------')
