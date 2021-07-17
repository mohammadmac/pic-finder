from time import sleep
from requests import get
from selenium import webdriver
from re import findall

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
    check_to_download(data)

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

def check_to_download(data):
    if data['width'] and data['height'] != '':
        both(data)
    elif data['height'] != '':
        height(data)
    elif data['width'] != '':
        width(data)

def both(data):
    try:
        count = 1
        found = 1
        while True:
            resolution_xpath = '//*[@id="zci-images"]/div/div[2]/div/div[%s]/div[3]' % count
            resolution = find(resolution_xpath).text
            
            pictre_width = int(resolution.split(' × ')[0])
            pictre_height = int(resolution.split(' × ')[1])

            count += 1
            if pictre_width >= int(data['width']) or pictre_height >= int(data['height']):
                print('\n%s- %s' % (found, resolution))
                pic_xpath = '//*[@id="zci-images"]/div[1]/div[2]/div/div[%s]/div[1]' % (count - 1)
                #driver.execute_script("arguments[0].scrollIntoView();", find(pic_xpath))
                find(pic_xpath).click()
                
                sleep(2)
                pic_url = find('//*[@id="zci-images"]/div[2]/div/div[1]/div[2]/div/div[2]/div/div/a').get_attribute('href')
                download(pic_url, data['save path'])
                
                found += 1
    except:
        print('\nDone! \n')

def width(data):
    try:
        count = 1
        found = 1
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
                download(pic_url, data['save path'])
                
                found += 1

    except:
        print('\nDone! \n')
        
def height(data):
    try:
        count = 1
        found = 1
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
                download(pic_url, data['save path'])

                found += 1
                
    except:
        print('\nDone! \n')

def download(pic_url, save_path):
    try:
        r = get(pic_url, stream=True)

        if "Content-Disposition" in r.headers.keys():
                file_name = findall("filename=(.+)", r.headers["Content-Disposition"])[0]
        else:
            file_name = pic_url.split("/")[-1]
            
        save_path = save_path + '/' + file_name

        if r.status_code == 200:
            total_size = int(r.headers.get('content-length', 0))
            stored = 0
            remaining_mark = 50 * '⡀'
            received_mark = '█'

            with open(save_path, 'wb') as file:
                for data in r.iter_content(chunk_size=1024):
                    outputfile = file.write(data)
                    
                    stored += outputfile
                    bar_amount = str((int(stored)/total_size) * 50)
                    bar_amount = (int(bar_amount.split('.')[0]) * received_mark) + remaining_mark[int(bar_amount.split('.')[0]):]
                    received = format((int(stored) / total_size) * 100, '.1f') +'%'
                    total_size_mb = format(total_size/1048576, '.1f') + 'MB'
                    bar_func(file_name, received, bar_amount, total_size_mb)
        else:
            print('Cannot download %s!' % (file_name))
            print('So it will open in another tab to download that yourself')
            driver.execute_script("window.open('%s','_blank')" % pic_url)
            sleep(2)
            driver.switch_to_window(driver.window_handles[0])

    except:
        print('Cannot download %s!' % (file_name))
        driver.execute_script("window.open('%s','_blank')" % pic_url)
        print('So it will open in another tab to download that yourself')
        sleep(2)
        driver.switch_to_window(driver.window_handles[0])

def bar_func(file_name, received, bar_amount, total_size):
    print('downloading %s |%s| %s %s' % (file_name, bar_amount, received, total_size), end='\r')
    if bar_amount == '██████████████████████████████████████████████████':
        print('Downloading %s |%s | %s - %s Done!' % (file_name, bar_amount, received, total_size))

def exit_func():
    print('exiting program...')
    exit()