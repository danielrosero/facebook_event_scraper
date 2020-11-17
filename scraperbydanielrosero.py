import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from pathlib import Path
import os
from datetime import date

#FES part
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep

#Tkinter
import tkinter as tk

today = date.today()
date = today.strftime("%d-%m-%Y")



# scrape one individual event
def event_info(driver, link):
    # example link = https://www.facebook.com/events/3102548586466148
    main_window_handle = driver.current_window_handle
    driver.execute_script(f'window.open("{link}","_blank");')
    driver.switch_to.window(driver.window_handles[1])

    try:
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='mount_0_0']/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/h2/span/span/span"))).text
    except TimeoutException:
        print("Can't find any title of event in 10 seconds")

    # find hosts (can be more than one)
    hosts = []
    for h in driver.find_elements_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div[1]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div/div/span/strong'):
        hosts += [h.text]
    time = driver.find_element_by_xpath(
        "//*[@id='mount_0_0']/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/h2/span").text
    going = driver.find_element_by_xpath(
        '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div[1]/div/div/div[2]/div[2]/div[last()]/div/div/div/div[2]/div/div[1]/div[1]/span[1]').text
    interested = driver.find_element_by_xpath(
        '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div[1]/div/div/div[2]/div[2]/div[last()]/div/div/div/div[2]/div/div[2]/div[1]/span[1]').text
    image = driver.find_elements_by_xpath(
        '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div/a/div/div/div/div/img')
    if image:
        image = image[0].get_attribute("src")
    location = driver.find_element_by_xpath(
        "//*[@id='mount_0_0']/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[3]/span/span").text
    ticket = driver.find_elements_by_xpath(
        '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div[1]/div/div/div[2]/div[2]/div[1]/div/div/div/div[2]/a')
    if ticket:
        ticket = ticket[0].get_attribute('href')
    details_bottom = driver.find_element_by_xpath(
        "//*[@id='mount_0_0']/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div[1]/div/div/div[1]/div[1]/div/div/div/div[last()]")
    categories = details_bottom.find_elements_by_css_selector(
        'div.lhclo0ds')
    if categories:
        categories = categories[0].text.split('\n')
    see_more = driver.find_elements_by_xpath(
        '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div/div[1]/div/div/div[1]/div[1]/div/div/div/div/span/div/div')

    # if 'See More', click
    if see_more:
        driver.execute_script("arguments[0].click();", see_more[0])
    sleep(1)
    description = details_bottom.find_element_by_css_selector('span').text
    # if see more, delete 'See Less' from description
    if see_more:
        description = description[:-9]

    driver.close()
    driver.switch_to.window(main_window_handle)
    return {
        "hosts": hosts,
        "title": title,
        "time": time,
        "description": description,
        "location": location,
        "ticket": ticket,
        "link": link,
        "image": image,
        "interested": interested,
        "going": going,
        "categories": categories
    }
 




def keywords_method():

    usr = e1.get()
    pwd = e2.get()
     
    url = "https://m.facebook.com/login.php?next=https://m.facebook.com/pg/{}/events/".format(e3.get())

    # url = "https://m.facebook.com/login.php?next=https://m.facebook.com/SpecializedBo/events/"

    # myTargetKeywords = ['Hercules & Love Affair','Miami','streaming']

    myTargetKeywords = e4.get().split(',')

    print(myTargetKeywords)


    driver = webdriver.Chrome('chromedriver')
    driver.get(url)

     

    elem = driver.find_element_by_id("m_login_email")
    elem.send_keys(usr)
     
    elem = driver.find_element_by_id("m_login_password")
    elem.send_keys(pwd)
     
    elem.send_keys(Keys.RETURN)
     

    events_scraped = [] 

     
    time.sleep(5)



    # INFINITE SCROLL

    SCROLL_PAUSE_TIME = 5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("TERMINO")

            break
        last_height = new_height

        # Scrap data

        # events = driver.find_elements_by_xpath("//*[@class='_592p _r-i']")
         
        # for event in events:
        #     if event.text not in events_scraped:
        #         events_scraped.append(event.text)

        # print(events_scraped)

        eventNames = driver.find_elements_by_xpath("//*[@class='_592p _r-i']")

        eventLinks = driver.find_elements_by_xpath("//*[@class='_5379']")

        i=0 



        # KEYWORDS MODE

        filePath=os.getcwd()+'/results/keys_'+'-'.join(myTargetKeywords)+'/'+date+'/'

        Path(filePath).mkdir(parents=True, exist_ok=True)

        for link in eventLinks:

            # print("Event Name: ",eventNames[i].text)
            # print("Event Link: ",link.get_attribute('href').replace("/m.", "/"))
            # print("******")
            cleanLink = link.get_attribute('href').replace("/m.", "/").split("?acontext")
            # print("CLEAN Link: ",cleanLink[0])

            for key in myTargetKeywords:
                if(key.lower() in eventNames[i].text.lower()):
                    print("MATCH Event with key: ", key," Event NAME: ",eventNames[i].text)

                    if eventNames[i].text not in events_scraped:
                        events_scraped.append(eventNames[i].text)
                        try:
                            result = event_info(driver,cleanLink[0])
                            print("JSON EventData: ", result)

                            with open(filePath+eventNames[i].text+'.json', 'w') as f:
                                json.dump(result, f)

                        except Exception as e:
                            print(".-.ERROR.-.",e)
                        else:
                            print(".-.SCRAPED.-.")

                        driver.switch_to_window(driver.window_handles[0])
                        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                
            print("****** || ******")
            i+=1

        i=0

        print("****** |SCROLLED TO BOTTOM| ******")






def bruteForce_method():

    usr = e1.get()
    pwd = e2.get()
     
    url = "https://m.facebook.com/login.php?next=https://m.facebook.com/pg/{}/events/".format(e3.get())

    # url = "https://m.facebook.com/login.php?next=https://m.facebook.com/SpecializedBo/events/"

    # myTargetKeywords = ['Hercules & Love Affair','Miami','streaming']

    myTargetKeywords = e4.get().split(',')

    print(myTargetKeywords)


    driver = webdriver.Chrome('chromedriver')
    driver.get(url)

     

    elem = driver.find_element_by_id("m_login_email")
    elem.send_keys(usr)
     
    elem = driver.find_element_by_id("m_login_password")
    elem.send_keys(pwd)
     
    elem.send_keys(Keys.RETURN)
     

    events_scraped = [] 

     
    time.sleep(5)



    # INFINITE SCROLL

    SCROLL_PAUSE_TIME = 5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("TERMINO")

            break
        last_height = new_height

        # Scrap data

        # events = driver.find_elements_by_xpath("//*[@class='_592p _r-i']")
         
        # for event in events:
        #     if event.text not in events_scraped:
        #         events_scraped.append(event.text)

        # print(events_scraped)

        eventNames = driver.find_elements_by_xpath("//*[@class='_592p _r-i']")

        eventLinks = driver.find_elements_by_xpath("//*[@class='_5379']")

        i=0 


        # # BRUTE FORCE TRYING TO SCRAP ALL THE EVENTS


        filePath=os.getcwd()+'/results/bruteForce/'+date+'/'

        Path(filePath).mkdir(parents=True, exist_ok=True)



        eventNames = driver.find_elements_by_xpath("//*[@class='_592p _r-i']")

        eventLinks = driver.find_elements_by_xpath("//*[@class='_5379']")

        i=0 

        for link in eventLinks:
            # print(element.get_attribute('href'))
            # print(element.text)


            if eventNames[i].text not in events_scraped:
                print("Event Name: ",eventNames[i].text)
                print("Event Link: ",link.get_attribute('href').replace("/m.", "/"))
                print("******")
                cleanLink = link.get_attribute('href').replace("/m.", "/").split("?acontext")
                print("CLEAN Link: ",cleanLink[0])
                events_scraped.append(eventNames[i].text)
                try:
                    result = event_info(driver,cleanLink[0])
                    print("JSON EventData: ", result)

                    with open(filePath+eventNames[i].text+'.json', 'w') as f:
                        json.dump(result, f)


                except Exception as e:
                    print(".-.ERROR.-.",e)
                else:
                    print(".-.SCRAPED.-.")

                # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                driver.switch_to_window(driver.window_handles[0])
                
            print("****** || ******")
            i+=1

        print("****** |SCROLLED TO BOTTOM| ******")
        i=0


master = tk.Tk()
master.config(bg='#202225')
master.resizable(0,0)
master.title('TEAM B Facebook Event Scraper')

tk.Label(master, text="Login", bg='#202225', fg='white').grid(row=0)
tk.Label(master, text="Password", bg='#202225', fg='white').grid(row=1)
tk.Label(master, text="FB Page Name", bg='#202225', fg='white').grid(row=2)
tk.Label(master, text="Event Keywords (separate with comma)", bg='#202225', fg='white').grid(row=3)

e1 = tk.Entry(master)
e1.config(bg='#202225',highlightbackground='#202225',fg='white')
e2 = tk.Entry(master)
e2.config(bg='#202225',highlightbackground='#202225',fg='white',show="*")
e3 = tk.Entry(master)
e3.config(bg='#202225',highlightbackground='#202225',fg='white')
e4 = tk.Entry(master)
e4.config(bg='#202225',highlightbackground='#202225',fg='white')

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)

tk.Button(master, text='Go BruteForce Scrap', command=bruteForce_method, highlightbackground='#202225').grid(row=4, column=0, sticky=tk.W, pady=4)
tk.Button(master, text='Go Keywords Scrap', command=keywords_method, highlightbackground='#202225').grid(row=4, column=1, sticky=tk.W, pady=4)

tk.mainloop()



