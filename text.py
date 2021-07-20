from time import sleep
from selenium import webdriver

def browser():
    global driver, find
    driver = webdriver.Chrome()
    find = driver.find_element_by_xpath

def search(data):
    browser()
    print('\nSearching for * %s *' % (data['search word']))
    driver.get(data['url'])
    sleep(2)
    scroll()
    check_to_store(data)
    
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

def check_to_store(data):
    if data['width'] and data['height'] != '':
        both(data)
    elif data['height'] != '':
        height(data)
    elif data['width'] != '':
        width(data)

def both(data):
    store_file_path = data['save path'] + '/' + data['search word'] + '.txt'

    try:
        count = 1
        found = 1
        store_file = open(store_file_path, 'a')
        while True:
            resolution_xpath = '//*[@id="zci-images"]/div/div[2]/div/div[%s]/div[3]' % count
            resolution = find(resolution_xpath).text
            
            pictre_width = int(resolution.split(' × ')[0])
            pictre_height = int(resolution.split(' × ')[1])
            
            count += 1
            if pictre_width >= int(data['width']) or pictre_height >= int(data['height']):
                print('\n%s- %s' % (found, resolution))
                pic_xpath = '//*[@id="zci-images"]/div[1]/div[2]/div/div[%s]/div[1]' % (count - 1)
                find(pic_xpath).click()
                
                sleep(2)
                pic_url = find('//*[@id="zci-images"]/div[2]/div/div[1]/div[2]/div/div[2]/div/div/a').get_attribute('href')
                print('link: ' + pic_url)
                pic_data = '\n' + str(found) + ' - ' + str(resolution) + '\n' + 'link: ' + pic_url + '\n'
                store_file.write(pic_data)
                
                found += 1

    except:
        store_file.close()
        print('\nDone! \n')

def width(data):
    store_file_path = data['save path'] + '/' + data['search word'] + '.txt'

    try:
        count = 1 
        found = 1
        store_file = open(store_file_path, 'a')
        while True:
            resolution_xpath = '//*[@id="zci-images"]/div/div[2]/div/div[%s]/div[3]' % count
            resolution = find(resolution_xpath).text
            
            pictre_width = int(resolution.split(' × ')[0])
            
            count += 1
            if pictre_width >= int(data['width']):
                print('\n%s- %s' % (found, resolution))
                pic_xpath = '//*[@id="zci-images"]/div[1]/div[2]/div/div[%s]/div[1]' % (count - 1)
                find(pic_xpath).click()
                
                sleep(2)
                pic_url = find('//*[@id="zci-images"]/div[2]/div/div[1]/div[2]/div/div[2]/div/div/a').get_attribute('href')
                print('link: ' + pic_url)
                pic_data = '\n' + str(found) + ' - ' + str(resolution) + '\n' + 'link: ' + pic_url + '\n'
                store_file.write(pic_data)

                found += 1

    except:
        store_file.close()
        print('\nDone! \n')

def height(data):
    store_file_path = data['save path'] + '/' + data['search word'] + '.txt'

    try:
        count = 1
        found = 1
        store_file = open(store_file_path, 'a')
        while True:
            resolution_xpath = '//*[@id="zci-images"]/div/div[2]/div/div[%s]/div[3]' % count
            resolution = find(resolution_xpath).text
            
            pictre_height = int(resolution.split(' × ')[1])
            
            count += 1
            if pictre_height >= int(data['height']):
                print('\n%s- %s' % (found, resolution))
                pic_xpath = '//*[@id="zci-images"]/div[1]/div[2]/div/div[%s]/div[1]' % (count - 1)
                find(pic_xpath).click()
                
                sleep(2)
                pic_url = find('//*[@id="zci-images"]/div[2]/div/div[1]/div[2]/div/div[2]/div/div/a').get_attribute('href')
                print('link: ' + pic_url)
                pic_data = '\n' + str(found) + ' - ' + str(resolution) + '\n' + 'link: ' + pic_url + '\n'
                store_file.write(pic_data)

                found += 1

    except:
        store_file.close()
        print('\nDone! \n')

def exit_func():
    print('exiting program...')
    exit()