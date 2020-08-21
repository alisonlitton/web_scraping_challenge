from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit MarsNews
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Get the average temps
    avg_temps = soup.find('div', id='weather')
    # Get the latest news title and paragraph
    news_titles = soup.find_all('div', class_='content_title')
    paragraph_text = soup.find_all('div', class_='article_teaser_body')
    news_title = news_titles[0].text
    news_p = paragraph_text[0].text


    #Visit JPL
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    time.sleep(1)
    #click to get full image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')
    #scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')
    #find the featured image 
    img_result = soup.find_all('figure', class_='lede')
    img_path = img_result[0].a['href']
    feat_img = 'https://www.jpl.nasa.gov/spaceimages' + img_path


    #visit MarsFacts
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    time.sleep(1)
    df = tables[0]
    df.columns = ['Fact', 'Value']
    mars_table = df.to_html()

    #visit MarsHemi page
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_names = []
    hemi_results = soup.find_all('div', class_='collapsible results')
    hemispheres = hemi_results[0].find_all('h3')
    for name in hemispheres:
        hemisphere_names.append(name.text)  
    thumb_results = hemi_results[0].find_all('a')
    thumb_links = []

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
        "hemis": hemi_dict
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data