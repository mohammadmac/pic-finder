import os
from re import S
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
find = driver.find_element_by_xpath

def Search(): 
    global search_word
    search_word = input('Enter word: ')
    search_word_url = search_word.replace(' ', '+')
    url = 'https://duckduckgo.com/?q={}&t=h_&iar=images&iaf=size%3AWallpaper&iax=images&ia=images'.format(search_word_url)
    driver.get(url)
    print('\nSearching for * %s *' % (search_word))
    sleep(2)
    Make_folder()
    
def Make_folder():
    global folder_path
    folder_name = ('\\' + search_word)
    folder_path = str(os.path.dirname(os.path.realpath(__file__))) + '\\downloads' + folder_name
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    Scroll()

def Scroll():
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        sleep(2)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
    sleep(10)
    Select_to_download()

def Select_to_download():
    global act
    print('\nDownload: ')
    print('1 - Wider pictures')
    print('2 - Higher pictures')
    print('3 - Both')
    print('0 - exit')
    act = input('--> ')
    
    if act == '1':
        Width()
    elif act == '2':
        Height()
    elif act == '3':
        Width()
        Height()
    elif act == '0':
        pass
    else:
        print('Input is incorrect. Try again. ')
        Again()

def Width():
    print('\n-------------------------------------------------------')
    print('\n      ...::: Width :::...')
    try:
        count = 1 
        while True:
            resolution_xpath = '//*[@id="zci-images"]/div/div[2]/div/div[%s]/div[3]' % count
            resolution = find(resolution_xpath).text
            width_1 = width(resolution)
            count += 1
            if width_1 >= 5000:
                print('\n..........%s..........' % (count - 1))
                pic_xpath = '//*[@id="zci-images"]/div/div[2]/div/div[%s]' % (count - 1)
                find(pic_xpath).click()
                sleep(2)
                pic_url = find('//*[@id="zci-images"]/div[2]/div/div[1]/div[2]/div/div[2]/div/div/a').get_attribute('href')
                print('Resolution: ' + resolution)
                print('link: ' + pic_url)
                print('Downloading:')
                file_name = filename(pic_url)
                try:
                    download(pic_url, file_name)
                    print('\n' + file_name + ' downloaded')
                except:
                    print('\nCannot download!')
                    driver.execute_script("window.open('%s','_blank')" % pic_url)
                    sleep(2)
                    driver.switch_to_window(driver.window_handles[0])
                    pass
    except:
        if act == '1':
            print('\nDone! \n')
            Again()
        else:
            pass

def width(resolution):
    count = 0
    for x in resolution:
        if x == '×':
            width_1 = resolution[:count]
        count += 1
    width_1 = int(width_1)
    return width_1

def Height():
    print('\n-------------------------------------------------------')
    print('\n      ...::: Height :::...')
    try:
        count = 1
        while True:
            resolution_xpath = '//*[@id="zci-images"]/div/div[2]/div/div[%s]/div[3]' % count
            resolution = find(resolution_xpath).text
            height_1 = height(resolution)
            count += 1
            if height_1 >= 5000:
                print('\n..........%s..........' % (count - 1))
                pic_xpath = '//*[@id="zci-images"]/div[1]/div[2]/div/div[%s]/div[1]' % (count - 1)
                find(pic_xpath).click()
                sleep(2)
                pic_url = find('//*[@id="zci-images"]/div[2]/div/div[1]/div[2]/div/div[2]/div/div/a').get_attribute('href')
                print('Resolution: ' + resolution)
                print('link: ' + pic_url)
                print('Downloading:')
                file_name = filename(pic_url)
                try:
                    download(pic_url, file_name)
                    print('\n' + file_name + ' downloaded')
                except:
                    print('\nCannot download!')
                    driver.execute_script("window.open('%s','_blank')" % pic_url)
                    sleep(2)
                    driver.switch_to_window(driver.window_handles[0])
                    pass
    except:
        print('\nDone! \n')
        Again()

def height(resolution):
    count = 0
    for x in resolution:
        if x == '×':
            height_1 = resolution[count+1:]
        count += 1
    height_1 = int(height_1)
    return height_1

def filename(pic_url):
    count = 1
    revers_url = pic_url[::-1]
    for i in revers_url:
        if i == '/':
            name = revers_url[:count-1]
            file_name = name[::-1]
            if file_name[-4] != '.':
                file_name = file_name + '.jpg'
            print(file_name)
            break
        count += 1
    return file_name

def download(pic_url, file_name):
    save_path = folder_path + '\\' + file_name
    with open(save_path, 'wb') as outfile:
        r = requests.get(pic_url)
        outfile.write(r.content)

def Again():
    print('Do you want search again?')
    print('1 - Search')
    print('2 - search for current searched title')
    print('0 - Exit')
    act = input('--> ')
    if act.lower() in ['1', 'search']:
        Search()
    elif act == '2':
        Select_to_download()
    elif act.lower() in ['0', 'exit']:
        exit_func()    
    else:
        print('Input is incorrect. Try again. ')
        Again()

def exit_func():
    print('exiting program...')
    exit()

Search()
