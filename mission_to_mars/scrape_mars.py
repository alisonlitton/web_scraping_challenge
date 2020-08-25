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
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)
    # Scrape page into Soup
    html = browser.html
    news_soup = bs(html, "html.parser")


    # Get the latest news title and paragraph
    news_title = news_soup.find('div', class_='content_title').text
    p_text = news_soup.find('div', class_='article_teaser_body').text

    browser.quit()


    #Visit JPL
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    browser.is_element_present_by_css("div.carousel_items", wait_time = 1)

    #scrape into soup
    html = browser.html
    jpl_soup = bs(html, "html.parser")

    #find the featured image 
    img_path = jpl_soup.find('a', class_='button fancybox').get('data-fancybox-href').strip()
    base_url = "https://www.jpl.nasa.gov"
    feat_img = base_url + img_path

    browser.quit()


    #visit MarsFacts
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    
    #scrape into soup
    html=browser.html
    facts_soup = bs(html, "html.parser")

    mars_table = pd.read_html(mars_facts_url)
    df=mars_table[0]

    mars_facts=df.rename(columns={0:'',1:'Mars'})
    mars_table_html = mars_facts.to_html()
    mars_table_html.replace('\n', '')
    mars_html = mars_facts.to_html('mars_facts.html', index=False)

    browser.quit()

    #visit MarsHemi page
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_hemi_url = "https://astrogeology.usgs.gov"
    browser.visit(hemi_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time = 1)

    html=browser.html
    time.sleep(12)
    hemi_soup = bs(html, "html.parser")
    
    hemi_results = hemi_soup.find("div", class_="result-list")
    hemi_item = hemi_results.find_all("div", class_="item")

    hemi_imgs = []

    for i in range(4):
        try:
            time.sleep(1)
            img_title = i.find("h2", class_="title").text
            hemi_img_url = i.fins("a")["href"]
            img_url = base_hemi_url + hemi_img_url

            browser.visit(img_url)
            img_html = browser.html
            img_soup = bs(img_html, "html.parser")
            img = img_soup.find("img", class_="wise-image")["src"]
            full_img = base_hemi_url + img
            mars_hemi_imgs.append({
                "image_title":img_title,
                "img_link":full_img
            })
        except Exception as e:
            print(e)
        browser.quit()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title ,
        "news_p": p_text ,
        "feat_img": feat_img ,
        "mars_facts": mars_html ,
        "hemi_imgs": hemi_imgs
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data