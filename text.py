import os
from time import sleep

from selenium import webdriver

driver = webdriver.Chrome()
find = driver.find_element_by_xpath

def search():
    global search_word
    global txt_path
    search_word = input('Enter word: ')
    file_name = '\\' + search_word + '.txt'
    txt_path = str(os.path.dirname(os.path.realpath(__file__))) + '\\text files' + file_name
    search_word_url = search_word.replace(' ', '+')
    url = 'https://duckduckgo.com/?q={}&t=h_&iar=images&iaf=size%3AWallpaper&iax=images&ia=images'.format(search_word_url)
    driver.get(url)
    print('Search resulf for * %s *' % (search_word), file=open(txt_path, "a"))
    sleep(2)
    scroll()
    
def scroll():
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        sleep(2)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
    sleep(10)
    Width()

def Width():
    print('\n      ...::: Width :::...', file=open(txt_path, "a"))
    try:
        count = 1 
        while True:
            resolution_xpath = '//*[@id="zci-images"]/div/div[2]/div/div[%s]/div[3]' % count
            resolution = find(resolution_xpath).text
            width_1 = width(resolution)
            count += 1
            if width_1 >= 5000:
                print('\n..........%s..........' % (count - 1), file=open(txt_path, "a"))
                pic_xpath = '//*[@id="zci-images"]/div/div[2]/div/div[%s]' % (count - 1)
                find(pic_xpath).click()
                sleep(2)
                pic_url = find('//*[@id="zci-images"]/div[2]/div/div[1]/div[2]/div/div[2]/div/div/a').get_attribute('href')
                print('Resolution: ' + resolution, file=open(txt_path, "a"))
                print('link: ' + pic_url, file=open(txt_path, "a"))
    except:
        Height()

def width(resolution):
    count = 0
    for x in resolution:
        if x == '×':
            width_1 = resolution[:count]
        count += 1
    width_1 = int(width_1)
    return width_1

def Height():
    print('\n-------------------------------------------------------', file=open(txt_path, "a"))
    print('\n      ...::: Height :::...', file=open(txt_path, "a"))
    try:
        count = 1
        while True:
            resolution_xpath = '//*[@id="zci-images"]/div/div[2]/div/div[%s]/div[3]' % count
            resolution = find(resolution_xpath).text
            height_1 = height(resolution)
            count += 1
            if height_1 >= 5000:
                print('\n..........%s..........' % (count - 1), file=open(txt_path, "a"))
                pic_xpath = '//*[@id="zci-images"]/div[1]/div[2]/div/div[%s]/div[1]' % (count - 1)
                find(pic_xpath).click()
                sleep(2)
                pic_url = find('//*[@id="zci-images"]/div[2]/div/div[1]/div[2]/div/div[2]/div/div/a').get_attribute('href')
                print('Resolution: ' + resolution, file=open(txt_path, "a"))
                print('link: ' + pic_url, file=open(txt_path, "a"))
    except:
        print('\nDone! \n')
        again()

def height(resolution):
    count = 0
    for x in resolution:
        if x == '×':
            height_1 = resolution[count+1:]
        count += 1
    height_1 = int(height_1)
    return height_1

def again():
    print('1 - Search')
    print('0 - Exit')
    act = input('--> ')
    if act.lower() in ['1', 'search']:
        search()
    elif act.lower() in ['0', 'exit']:
        exit_func()
    else:
        print('Input is incorrect. Try again. ')
        again()

def exit_func():
    print('exiting program...')
    exit()

search()
