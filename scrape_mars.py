from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    scrape_data = {}

    # 1: NASA MARS NEWS
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #time delay is so that page can load and all information can be scraped
    time.sleep(5)

    # To obtain the page html
    html = browser.html

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html, 'html.parser')

    # Collecting the latest title after identifying the tag and class from HTML
    result_title = soup.find('div', class_="content_title")

    # Cleaning up the title using the strip method
    news_title = result_title.text.strip()

    # Collecting the latest paragraph after identifying the tag asnd class from HTML
    result_paragraph = soup.find('div', class_="article_teaser_body")

    # Cleaning up the paragraph using the strip method
    news_p = result_paragraph.text.strip()

    scrape_data['news_title'] = news_title
    scrape_data['news_p'] = news_p
   
    # 2: Featured Image
    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # time delay is so that page can load and all information can be scraped
    time.sleep(5)

    # Clicking on 'Full Image' Button
    browser.click_link_by_partial_text('FULL IMAGE')

    #time delay is so that page can load and all information can be scraped
    time.sleep(5)

    # Clicking on 'more info' Button
    browser.click_link_by_partial_text('more info')

    #time delay is so that page can load and all information can be scraped
    time.sleep(5)

    # To obtain the page html
    html = browser.html

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get the latest image
    latest_image = soup.find('figure', class_="lede")

    # Get the link of the latest image
    link = latest_image.a['href']

    # Full Link to Image
    featured_image_url = 'https://www.jpl.nasa.gov' + link

    scrape_data['image'] = featured_image_url

    # 3: Mars Weather
    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    #time delay is so that page can load and all information can be scraped
    time.sleep(5)

    # To obtain the page html
    html = browser.html

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html, 'html.parser')

    # Collecting the latest paragraph after identifying the tag asnd class from HTML
    latest_tweet = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    # Cleaning up the paragraph using the strip method
    mars_weather = latest_tweet.text.strip()

    scrape_data['weather_data'] = mars_weather

    # 4: Mars Facts
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing 
    # facts about the planet including Diameter, Mass, etc.
    url = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(url , encoding= "utf-8")

    # Assign the columns ['Data Type', 'Measure']
    df = tables[0]
    df.columns = ['Data_Type', 'Measure']

    # Set the index to the Data Type Column
    df.set_index('Data_Type', inplace=True)

    # Pandas also had a to_html method that we can use to generate HTML tables from DataFrames.
    html_table = df.to_html()

    # You may have to strip unwanted newlines to clean up the table.
    html_table.replace('\n', '')
    
    scrape_data['mars_facts'] = html_table

    # 5:Mars Hemispheres
    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #time delay is so that page can load and all information can be scraped
    time.sleep(5)

    # To obtain the page html
    html = browser.html

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    # First, get a list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemisphere = {}
    
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
    
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text

        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
    
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
    
        # Finally, we navigate backwards
        browser.back()

    scrape_data['mars_hemispheres'] = hemisphere_image_urls

    return scrape_data
