# NewsApp

Flask and NewsAPI introduction
Flask: Flask is a web framework written in python which allows you to create server-side endpoints. You can learn more about flask from this link: https://www.geeksforgeeks.org/python-introduction-to-web-development-using-flask/.

NewsAPI: News API is a simple Rest API for retrieving live articles from all over the web. Using News API you can fetch top headlines of a country from a particular source like the Times of India, Hindustan Times, BBC News, and many more. We can also fetch articles related to a particular topic. visit https://newsapi.org/ for more information.

API key generation
In order to use the News API in our application, you will need to generate a unique API key from https://newsapi.org/. Visit this website and create your free account, on successful registration and email verification you will get your API key on the screen. While registering you may need to choose a developer plan (choose according to your requirements). Save this API key somewhere so that it can be used further.

Flask and NewsAPI installation
simply install Flask using the pip command :

pip install flask 

After successful installation creates one folder for application name this folder flask_news or anything else of your choice. Inside this folder create a new file called app.py. We will write our entire back-end code in this file in the upcoming steps.

To install NewsAPI we will use a pip command like this :

pip install newsapi-python

You can learn more about the newsapi-python library from here: https://newsapi.org/docs/client-libraries/python
