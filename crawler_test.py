from bs4 import BeautifulSoup
import requests
from random import shuffle
import random
import time
import sys
import json
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

url = 'https://gartic.io/'

# adblock options
chop = webdriver.ChromeOptions()
chop.add_extension('Adblock_Plus.crx')

# chrome driver
driver = webdriver.Chrome(chrome_options = chop)
driver.get(url)

# username
name = '別問我痛匴甚麼'

# Enter game button
def StartGame():
    try:
        # enter username
        user_nme = driver.find_element_by_css_selector('input')
        user_nme.clear()
        user_nme.send_keys(name)

        btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btYellowBig.ic-playHome")))
        btn.click()
        # bullshit advertisement
        btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#gphone > button")))
        btn.click()
        # ok button enter
        ok_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btYellowBig.ic-yes")))
        ok_btn.click()
    except:
        print('Start Game Fail!')

# Add debug buttion, run js
def AddBtn():
    js = """
        var input = document.createElement('input');
        input.setAttribute('id', 'fghbvc');
        input.type = 'text';
        input.value = 'save';
        document.querySelector('#screenRoom').appendChild(input);

        var input2 = document.createElement('input');
        input2.setAttribute('id', 'fghbvc2');
        input2.type = 'text';
        document.querySelector('#chat > h5').appendChild(input2);

        var btn = document.createElement('button');
        btn.type = 'button'
        btn.innerHTML = 'click me';
        btn.onclick = function(){
                document.cookie = 'msg =' + input2.value;
                return false;
        };
        document.querySelector('#chat > h5').appendChild(btn);
        """
    driver.execute_script(js)

# Load data ans
with open('data.txt') as json_file:
    tot_ans = json.load(json_file)

StartGame()
AddBtn()

# Record time
play_time = 0

# Do magic
while True:
    # get html
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    # Reset status to save
    def ResetDebug():
        dg = driver.find_element_by_css_selector("#fghbvc")
        dg.clear()
        dg.send_keys('save')

    # enter cool msg, this is in the room
    try:
        word = driver.find_element_by_css_selector("#fghbvc").get_attribute("value")
        word2 = driver.find_element_by_css_selector("#fghbvc2").get_attribute("value")

        if word == 'player':
            # player name
            lt = set([e.text for e in soup.select('span.nick')])
            print(lt)
            ResetDebug()
        elif word == 'save':
            try:
                a, b = soup.select_one('div.msg.turn').text.split()
                if a == '這題的答案是:':
                    if b not in set(tot_ans[str(len(b))]):
                        print('答案是: ', b)
                        tot_ans[str(len(b))].append(b)
                        with open('data.txt', 'w') as outfile:
                            json.dump(tot_ans, outfile, ensure_ascii=False)
            except:
                pass
        elif word.startswith('go'):
            # guess ans, but maybe too fast
            try:
                _, b = word.split()
                hack = tot_ans[b].copy()
                shuffle(hack)
                ans_text = driver.find_element_by_css_selector('input.mousetrap')
                for e in hack[:10]:
                    try:
                        ans_text.clear()
                        ans_text.send_keys(e, Keys.ENTER)
                        time.sleep(0.45)
                    except:
                        break
                ResetDebug()
            except:
                print('too Fast!')
        elif word.startswith('tot'):
            # guess ans, but maybe too fast
            # careful use. maybe kick out room
            try:
                _, b = word.split()
                hack = tot_ans[b].copy()
                shuffle(hack)
                ans_text = driver.find_element_by_css_selector('input.mousetrap')
                for e in hack:
                    try:
                        ans_text.clear()
                        ans_text.send_keys(e, Keys.ENTER)
                        time.sleep(0.45)
                    except:
                        break
                ResetDebug()
            except:
                print('too Fast!')
        elif word.startswith('print'):
            try:
                _, b = word.split()
                # print dict
                print(tot_ans[b])
                ResetDebug()
            except:
                print('Nothing print')

        # Get Cookie
        try:
            word2 = driver.get_cookie('msg')['value']
            if word2:
                # Search pattern that is exist. send ans
                for bag in tot_ans.values():
                    for wd in bag:
                        if word2 in wd:
                            try:
                                ans_text = driver.find_element_by_css_selector('input.mousetrap')
                                ans_text.clear()
                                ans_text.send_keys(wd, Keys.ENTER)
                                time.sleep(0.45)
                            except:
                                break
            driver.delete_all_cookies()
            tmp = driver.find_element_by_css_selector("#fghbvc2")
            tmp.clear()
        except:
            pass
        
        # while game playing a long time
        try:
            ok_btn = driver.find_element_by_css_selector("button.btYellowBig.ic-yes")
            ok_btn.click()
            print('幫你點螢幕')
        except:
            pass

        # game drawing, display 2 word. 
        try:
            pop_up_ans = soup.select('div.word')
            if len(pop_up_ans) == 2:
                for e in pop_up_ans:
                    if len(e.text) > 0:
                        b = e.text[:-1]
                        if b not in set(tot_ans[str(len(b))]):
                            print('答案是: ', b)
                            tot_ans[str(len(b))].append(b)
                            with open('data.txt', 'w') as outfile:
                                json.dump(tot_ans, outfile, ensure_ascii=False)
        except:
            pass
        
        # # Auto Guess Ans
        # try:
        #     wd_span = soup.select_one('div.word')
        #     ans_text = driver.find_element_by_css_selector('input.mousetrap')
        #     ans_text.clear()
        #     ans_text.send_keys(random.choice(tot_ans[str(len(wd_span))]), Keys.ENTER)
        #     time.sleep(2.5)
        # except:
        #     pass

        # try:
        #     if '面面拒盜' in set([e.text for e in soup.select('span.nick')]):
        #         has = True
        # except:
        #     pass

        # 60 minutes Go out.
        if play_time >= 60*60:
            play_time = 0
            # try:
            #     gg = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#exit")))
            #     gg.click()
            #     exit_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btYellowBig.smallButton.ic-yes')))
            #     exit_btn.click()
                
            #     print('~換房囉~')
            #     time.sleep(2.5)
            # except:
            #     print('Go out fail...')

    except:
        # if go out homepage, restart
        driver.refresh()
        StartGame()
        AddBtn()

    time.sleep(2.5)
    play_time += 2.5
    
driver.close()

