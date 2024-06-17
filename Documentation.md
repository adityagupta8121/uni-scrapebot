# University Website Scraper and AI Chatbot

## Requirements

A web application where users can input a university website link. 
1. The application should scrape the website to find all internal domain links and documents, categorize them, and list them.
2. Implement a search feature to allow users to search across different categories of documents.
3. Bonus Feature: Implement Pagination
4. Integrate an AI chatbot that can answer questions based on the scraped text information. 

### Requirements not fulfilled
1. Integrating the AI chatbot in the same app.
2. Training the chatbot on the scraped text information. (the correct use of LLM)
3. The use of Tailwind CSS
4. The use of database - Postgres

### Why the requirements were not fulfilled?
1. I was having issues with making the buttons work in react and Python and I was trying very hard to implement the LLM but that didn't work.
2. I wasn't able to have tailwind CSS Setup, I followed all the steps on the web but still was unsuccessful
3. Since the LLM was hard to implement, and therefore I had no data to be stored after that too, using a DB wouldn't have been beneficial.

## Fixes
1. Learn more about LLM (different models), and train the bot
2. Change styling to Tailwind CSS
3. The use of database to store all data
4. Combine the two apps

## Approach and Design Choices
I used Python for web-scraping and flask for the web-app. I was also able to figure out Ollama in Python which gave me the ability to integrate the chatbot too.

React and CSS were used for front-end, as mentioned in the specifications.

### Web Scraping:

The app accepts a university website URL and uses the Requests library to fetch the content of the page. BeautifulSoup parses the HTML content to extract all internal links. Links are categorized based on their types: PDFs, DOCs, and HTML pages.

- Backend:
Endpoints are defined to handle POST requests with a university URL.
Flask-CORS is used to allow the frontend to make requests to the backend.

- AI Chatbot:
The frontend collects user questions and the university URL.
The backend processes these inputs and uses the scraped data to generate responses.
Responses are filtered and returned to the frontend for display.

- Frontend:
React handles user input and displays the chat interface, and the scraped data.
Axios is used to send user questions and the university URL to the backend API.
Responses from the backend are displayed in the chat window and the results page, with URLs rendered as clickable links.

## Tools Used
- Requests
- BeautifulSoup
- React (have used only with JS)
- CSS
- Python

### Tools Used for the first time
- Flask
- Flask-CORS
- LLM - Ollama - Mistral
- Axios
- Tailwind CSS