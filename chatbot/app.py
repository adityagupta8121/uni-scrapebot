'''
University Website Scraper and AI Chatbot
Filename: app.py

Creates a web application using Flask that can fetch and process information 
from a given university URL and answer user questions based on the content of that URL

Tried to follow this tutorial closely: https://www.llamaindex.ai/blog/running-mixtral-8x7-locally-with-llamaindex-e6cebeabe0ab
Since Mixtral for Ollama needs heavy RAM requirements, I was unable to completely follow
and therefore it has limited functionality and was not able to fine-tune the AI model according to university website
I also added functionality to read from PDFs 
'''
from flask import Flask, request, jsonify
from flask_cors import CORS
from llama_index.llms.ollama import Ollama
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import re
import PyPDF2
from io import BytesIO

#initializing flask app with CORS and Ollama with mistral
app = Flask(__name__)
CORS(app)
llm = Ollama(model = "mistral")

#function to get internal links and documents from the url
def get_internal_links_and_documents(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    base_domain = urlparse(url).netloc
    links_with_titles = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)

        if parsed_url.netloc == base_domain: #check for internal links
            link_info = {'url': full_url, 'title': a_tag.get_text(strip=True)}
            links_with_titles.append(link_info)

    return links_with_titles

#function to extract text from each page of pdf
def get_text_from_pdf(url):
    response = requests.get(url)
    pdf_file = BytesIO(response.content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''

    for page in pdf_reader.pages:
        text += page.extract_text()

    return text

#check for a greeting, as ollama is slow on my laptop, this helps with the first basic prompt
def is_greeting(question):
    greetings = ["hi", "hello", "hey", "how are you", "what's up", "good morning", "good afternoon", "good evening"]
    if any(greeting in question.lower() for greeting in greetings):
        return True
    return False

#extract relevant sentences based on keywords
def extract_relevant_sentences(text, keywords, num_sentences=3):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    relevant_sentences = [sentence for sentence in sentences if any(word in sentence.lower() for word in keywords)]
    return ' '.join(relevant_sentences[:num_sentences])

#gets text based info from the url
def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    texts = [p.get_text() for p in paragraphs]
    return ' '.join(texts)

#function that takes care of questions, uses ollama model if the info isnt found in the extracted data
def answer_question(question, url):
    if is_greeting(question):
        return "Hello! How can I help you today?"

    meaningful_words = re.findall(r'\b\w{3,}\b', question.lower()) #check for words of specifc character
    if not meaningful_words:
        return "Please ask something more specific."

    links_with_titles = get_internal_links_and_documents(url)
    response = ""
    found_links = False

    all_text = get_text_from_url(url)

    for link in links_with_titles:
        title = link['title'].lower()
        if any(word in title for word in meaningful_words): #check title
            response += f"{link['title']}: {link['url']}\n"
            found_links = True

        if link['url'].endswith('.pdf'): #check pdf
            try:
                pdf_text = get_text_from_pdf(link['url'])
                all_text += ' ' + pdf_text
            except Exception as e:
                print(f"Error reading PDF {link['url']}: {e}")

    if any(word in all_text.lower() for word in meaningful_words):
        relevant_info = extract_relevant_sentences(all_text, meaningful_words)
        response += "\nRelevant information found on the website:\n"
        response += relevant_info + "\n"
        found_links = True

    if not found_links: #call ollama model if data isn't found
        response = str(llm.complete(question))

    return response

#endpoint defined to get info from university url
@app.route('/fetch_info', methods=['POST'])
def fetch_info():
    data = request.json
    university_url = data.get('university_url')

    if not university_url:
        return jsonify({'error': 'University URL is required.'}), 400

    links_with_titles = get_internal_links_and_documents(university_url)
    documents = [link for link in links_with_titles if link['url'].endswith('.pdf')]

    pdf_texts = {}
    for doc in documents:
        try:
            pdf_text = get_text_from_pdf(doc['url'])
            pdf_texts[doc['title']] = pdf_text
        except Exception as e:
            pdf_texts[doc['title']] = f"Error reading PDF: {str(e)}"

    return jsonify({
        'links_with_titles': links_with_titles,
        'pdf_texts': pdf_texts
    })

#endpoint defined to interact with the AI bot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    university_url = data.get('university_url')
    
    if not university_url:
        return jsonify({'error': 'University URL is required.'}), 400

    response = answer_question(user_input, university_url)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)