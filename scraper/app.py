'''
University Website Scraper and AI Chatbot
Filename: app.py

Creates a web application using Flask that can fetch and process internal links 
from a given university URL and give user the ability to search data, and also click on the links

Pagination was also implemented
'''
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import os
from flask_cors import CORS 

#initializing flask app with CORS
app = Flask(__name__)
CORS(app)

#function to get internal links and documents from the url
def get_internal_links_and_documents(url):
    response = requests.get(url) #make a request and get base domain
    soup = BeautifulSoup(response.content, 'html.parser')
    base_domain = urlparse(url).netloc
    
    pdf_links = []
    doc_links = []
    other_links = []

    #identify document types
    pdf_regex = re.compile(r'\.pdf$', re.IGNORECASE)
    doc_regex = re.compile(r'\.(doc|docx)$', re.IGNORECASE)
    
    #finding all links
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)
        
        #checking if internal
        if parsed_url.netloc == base_domain:
            link_info = {'url': full_url, 'title': a_tag.get_text(strip=True)}
            #categorizing on basis of file type
            if pdf_regex.search(full_url):
                #get file name from url
                filename = os.path.basename(parsed_url.path)
                link_info['filename'] = filename
                pdf_links.append(link_info)
            elif doc_regex.search(full_url):
                doc_links.append(link_info)
            elif full_url.endswith('/') or full_url.endswith('.html') or full_url.endswith('.htm'):
                #check for html pages
                try:
                    page_response = requests.get(full_url)
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')
                    title_tag = page_soup.find('title')
                    link_info['title'] = title_tag.get_text(strip=True) if title_tag else link_info['title']
                except requests.RequestException:
                    pass
                other_links.append(link_info)
            else:
                other_links.append(link_info)
    
    return pdf_links, doc_links, other_links

#endpoint defined to scrape the data from the website/given url
@app.route('/scrape', methods=['POST'])
def scrape_website():
    data = request.get_json()
    url = data['url']
    
    pdf_links, doc_links, other_links = get_internal_links_and_documents(url)
    
    #response in json format
    response = {
        'pdf_links': pdf_links,
        'doc_links': doc_links,
        'other_links': other_links
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)