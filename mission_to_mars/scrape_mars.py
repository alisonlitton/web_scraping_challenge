from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests 

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit MarsNews
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    news_soup = bs(html, "html.parser")


    # Get the latest news title and paragraph
    news_title = news_soup.find('div', class_='content_title').get_text()
    p_text = news_soup.find('div', class_='article_teaser_body').get_text()


    #Visit JPL
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)
    html = browser.html
    jpl_soup = bs(html, "html.parser")

    #find the featured image 
    img_path = jpl_soup.find('a', class_='button fancybox').get('data-fancybox-href')
    feat_img = jpl_url + img_path

    #visit MarsFacts
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    time.sleep(1)
    mars_facts = pd.read_html(mars_facts_url)
    df = mars_facts[0]
    mars_facts_df = df.rename(columns={0: "", 1: "Mars"})
    html_table = mars_facts_df.to_html()
    html_table.replace('\n', '')
    mars_table = mars_facts_df.to_html('mars_facts.html', index=False)
   

    #visit MarsHemi page
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    urls = [
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
        ]
    

    for thumb in thumb_results:
        if (thumb.img):
            img_url = 'https://astrogeology.usgs.gov' + thumb['href']
            thumb_links.append(img_url)
    
    full_img = []
    for url in thumb_links:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all('img', class_='wide-image')
        img_path = results[0]['src']
        img_link = 'https://astrogeology.usgs.gov' + img_path
        full_img.append(img_link)
    
    hemi_zip = zip(hemisphere_names,full_img)
    img_urls = []

    for title, img in hemi_zip:
        hemi_dict = {}
        hemi_dict['title'] = title
        hemi_dict['img_url'] = img
        img_urls.append(hemi_dict)
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title ,
        "news_p":news_p ,
        "feat_img": feat_img ,
        "mars_facts": mars_table ,
        "hemisphere_names": hemi_url
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data