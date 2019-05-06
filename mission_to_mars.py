
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd 
import pymongo
import urllib.request
from urllib.request import urlopen
import requests
import shutil
from pprint import pprint


# Set executable path and initialize chrome browser in splinter
def init_browser():
    executable_path = {"executable_path":'C:/ChromeSafe/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()


#scrape_info()

    print("start scrape_info")
    #Create empty dictionaries to store all the mars information.
    mars_info_dict=dict()


    executable_path = {'executable_path': 'C:/ChromeSafe/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # # Part 1 Visit the NASA mars news site

    # Visit NASA news Url
    url ="https://mars.nasa.gov/news/"
    browser.visit(url)


    html =browser.html
    soup = bs(html, 'html.parser')
    slide_elem = soup.select_one('ul.item_list li.slide')


    #slide_elem.find("div", class_='content_title').text
    slide_elem.find("div", class_='content_title')
    #news_title = article.find("div", class_="content_title").text


    # use the parent element to find the date in the article
    news_date = slide_elem.find("div", class_='list_date').get_text()
    news_date


    # use the parent element to find the first a tag and save it as news title
    news_title = slide_elem.find("div", class_='content_title').get_text()
    news_title


    # use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    news_p


    #Append results from part 1 into the final mars_info dictionary.
    mars_info_dict["Mars_news_date"] = news_date
    mars_info_dict["Mars_news_title"] = news_title
    mars_info_dict["Mars_news_body"] = news_p
    pprint(mars_info_dict)

    # # Part 2 JPL Space Images Featured Image

    # Visit the JPL Mars URL
    url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)


    html2 = browser.html
    soup2 = bs(html2, "html.parser")


    # Scrape the browser into soup and use soup to find the image of mars
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    # Save the image url to a variable called `img_url`


    # find the more info button and click
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()


    # This will parse the resulting html with soup
    html2 = browser.html
    soup2 = bs(html2, "html.parser")


    # find the relative image url
    #img_url_rel = soup2.select_one('figure.lede a img').get("src")
    img_url_rel = soup2.find('figure', class_='lede').a['href']
    img_url_rel_url = "https://www.jpl.nasa.gov" + img_url_rel
    print(img_url_rel_url)


    # Use the base url to create an absolute url
    #img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    #img_url


    #Append featured image url to the Mars dictionary.
    mars_info_dict["Mars_featured_image_url"] = img_url_rel_url


    pprint(mars_info_dict)

    # # 3 Visit the Mars Weather twitter account

    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)


    html3 = browser.html
    soup3 = bs(html3, "html.parser")


    # find tweet with data name for mars weather
    mars_weather = soup3.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather


    #Add weather tweet to the mars_info dict.
    mars_info_dict["Mars_tweet_weather"] = mars_weather


    pprint(mars_info_dict)

    # # 4 Mars Facts

    df = pd.read_html('https://space-facts.com/mars/')[0]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    df


    df.to_html("mars_facts.html", index=False)


    # Provide column names for the dataframe. 
    #df.columns = ['Mars_Facts', 'Values']

    #Use Pandas to convert the data to a HTML table string.
    df.to_html("mars_facts.html", index=False)

    #set index for better retrieval. 
    #df.set_index("Mars_Facts")
    mars_facts_html = df.to_html(classes="description table table-striped")


    mars_info_dict["Mars_facts_table"] = mars_facts_html


    pprint(mars_info_dict)

    # # 5 Visit the USGS Astogeology site and scrape pictures of the hemispheres

    import datetime


    url5 =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/"
    browser.visit(url5)


    time.sleep(5)
    html5 = browser.html
    soup5 = bs(html5, "html.parser")


    #parse soup object for images of the 4 hemispheres .
    class_collap_results = soup5.find('div', class_="collapsible results")
    astro_hemis_items = class_collap_results.find_all('div',class_='item')


    astro_hemis_items


    # get the list of all the hemispheres
    hemis_img_urls_list=list()
    img_urls_list = list()
    title_list = list()

    # Next loop through the links
    for i in astro_hemis_items:
        i_title = i.h3.text
        title_list.append(i_title)
        
        # find the href link.
        i_href  = "https://astrogeology.usgs.gov" + i.find('a',class_='itemLink product-item')['href']
        
        print(i_title,i_href)
        
        #browse the link from each page
        browser.visit(i_href)
        time.sleep(5)
        
        #Retrieve the  image links and store in a list. 
        html5   = browser.html
        soup_img = bs(html5, 'html.parser')
        i_img_url = soup_img.find('div', class_='downloads').find('li').a['href']
        print("i_img_url" + i_img_url)
        img_urls_list.append(i_img_url)
        
        # create a dictionary with  each image and title and append to a list. 
        hemispheres_dict = dict()
        hemispheres_dict['title'] = i_title
        hemispheres_dict['img_url'] = i_img_url
        
        hemis_img_urls_list.append(hemispheres_dict)
        
        #print(hemis_img_urls_list)
        #print(title_list)
        #print(img_urls_list)
        
        # finding the elements on each loop
        #browser.find_by_css("a.product-item h3")[i].click()
        
        # Next find the sample  image anchor tag and extract the href
        #Sample_elem = browser.find_link_by_text('Sample').first
        #asto_hemis['img_url'] = Sample_elem['href']
        
        # Get hemisphere title
        #asto_hemis['title'] = browser.find_by_css('h2.title').text
        
        # Append hemisphere object to list
        #hemis_image_urls.append(asto_hemis)
        # Navigate back
    #browser.back()


    #Add hemispheres list  to the mars_info dictionary.
    mars_info_dict["Hemisphere_image_urls"] = hemis_img_urls_list


    pprint(mars_info_dict)


    #retrieve article date and time and store it in the dictionary.
    art_datetime = datetime.datetime.utcnow()
    mars_info_dict["Date_time"] = art_datetime


    pprint(mars_info_dict)

    #Return final dictionary with all the mars information that was scraped in the 5 steps above. 
    print("just before final return of mars_info_dict")
    print(hemis_img_urls_list)
    mars_return_dict =  {
            "News_Title": mars_info_dict["Mars_news_title"],
            "News_Summary" :mars_info_dict["Mars_news_body"],
            "Featured_Image" : mars_info_dict["Mars_featured_image_url"],
            "Weather_Tweet" : mars_info_dict["Mars_tweet_weather"],
            "Facts" : mars_facts_html,
            "Hemisphere_Image_urls": hemis_img_urls_list,
            "Date" : mars_info_dict["Date_time"],
    }
    return mars_return_dict

#data_result = scrape_info()
#pprint(data_result)





