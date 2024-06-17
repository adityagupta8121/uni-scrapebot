# University Website Scraper and AI Chatbot

A web application developed using Python Flask and React where users can input a university website link.

---

## chatbot

The application scrapes the website text and links, and an AI chatbot answers questions based on the scraped information
- scrapes website and stores information
- checks the website for information
- calls ollama if information isn't present
- answers on the basis of keywords

## scraper

The application scrapes the website to find all internal domain links and documents, categorize them, and list them. Users can search by keywords and it also allows users to see different categories of documents.
- scrapes the website
- displays the results
- pagination is implemented
- search by keyword for easy search
- results are in the form of hyperlinks

---

### Technologies used
- Python with Flask (and other libraries)
- React
- CSS
- Ollama (Mistral)

---

### Run/Setup

Run Ollama Model Locally
```ollama run mistral```

Run Python Flask Server
```python app.py```

Start react!
```npm start```

App should run on 
```http://localhost:3000/```