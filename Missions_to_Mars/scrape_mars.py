#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
#pip install ipython
#pip install nbconver
import requests
import pandas as pd


#Site Navigation
def init_browser():
    executable_path = {"executable_path": "/Users/sharonsu/Downloads/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


#Mars News scrape function
def scrape():

    #dictionary to hold all scraped data:
    mars_data = {}

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve page with the requests module
    response = requests.get(url)
     # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    # results are returned as an iterable list
    results = soup.find_all("div", class_="slide")
    # Loop through returned results
    article_list = []
    for result in results:
    # Error handling
        # Identify and return title of article
         #time.sleep(3)
        news_title = result.find('div', class_="content_title")
        title = news_title.find('a').text
        # Identify and return description of article
        news_p = result.find('div', class_="rollover_description")
        description = news_p.find('div', class_="rollover_description_inner").text
        
        # Print results only if title, and link are available
        if (news_title and news_p):
            print('-------------')
            print(f'Article Title: {title}')
            article_list.append(result)
            print(f'Article Description: {description}')
            #description_list.append(result)
           
    
        #Print the latest news title and description
        print(f'Latest News Title: {title}')
        print(f'Description of Latest News Title: {description}')

    mars_data['news_title'] = title
    mars_data['news_desc'] = description

#Mars image scrape function Space Images - Featured Image
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('article', class_='carousel_item')
    #Loop through images to get partial url
    for image in images:
        image_url = image.find('a')['data-fancybox-href']
    #create varible for featured image url
    main_url = 'https://www.jpl.nasa.gov/'
    featured_image_url = main_url + image_url
    print(f"Click this link to see the current featured image: {featured_image_url}")

    mars_data['feature_image'] = featured_image_url

#Mars  Weather - not required



# Mars Facts scrape function
    #Create link for pandas URL
    pandas_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(pandas_url)
    df = tables[0]
    df.columns = ['Topic', 'Data']
    df.set_index(['Topic'])
    #Create html table
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')    

# Mars hemisphere scrape:
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url_start = 'https://astrogeology.usgs.gov'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #Create a loop to get the link to each page that will be looped through to collect title and image url  

    img_urls = []

    hems = soup.find_all('div', class_="item")

    for item in hems:
        link = item.find('a')
        href = link['href']
        url = url_start + href
        print(url)
        
        img_urls.append(url)
        
        #print(img_urls)      

       # print(final_data)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find all div classes 'item'
    hemispheres = soup.find_all('div', class_="item")

    # get list of URLs for each hemisphere
    img_url_text = []

    for item in hemispheres:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        
        link = item.find('a')
        href = link['href']
       
        #print('-----------')
        #print(header.text)
       
        url = ('https://astrogeology.usgs.gov' + href)
        #print(url)
        
        #dict = {'title':header.text}
        #titles.append(dict)
        img_url_text.append(url)

        hemisphere_image_urls = []
#title_list = []

    for url in img_url_text:
        #time.sleep(2)
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        titles = soup.find('h2',class_="title")
        browser.links.find_by_text('Sample')
        image = browser.windows[0].next.url
        
        urls = {
            'title':titles.text,
            'img_url':image
        }

          
        #title_list.append(titles)
        hemisphere_image_urls.append(urls)
        
        print(titles.text)
        print(image)
        print('-----------')

        print(hemisphere_image_urls)

    mars_data['images'] = urls

    browser.quit()

    return mars_data