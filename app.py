# import libraries
from flask import Flask, render_template, request
from newsapi import NewsApiClient

# init flask app
app = Flask(__name__)

# Init news api 
newsapi = NewsApiClient(api_key='c7ceb304f7de46b091b25f6096a1e515')

# helper function
def get_sources_and_domains():
    all_sources = newsapi.get_sources()['sources']
    sources = []
    domains = []
    for e in all_sources:
        id = e['id']
        domain = e['url'].replace("http://", "")
        domain = domain.replace("https://", "")
        domain = domain.replace("www.", "")
        slash = domain.find('/')
        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)
    return sources, domains

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        sources, domains = get_sources_and_domains()
        keyword = request.form["keyword"]
        
        # Making the first call without sources and domains if they are too many
        if len(sources) > 20 or len(domains) > 20:
            related_news = newsapi.get_everything(q=keyword,
                                                  language='en',
                                                  sort_by='relevancy')
        else:
            sources_str = ", ".join(sources)
            domains_str = ", ".join(domains)
            related_news = newsapi.get_everything(q=keyword,
                                                  sources=sources_str,
                                                  domains=domains_str,
                                                  language='en',
                                                  sort_by='relevancy')
        
        no_of_articles = related_news['totalResults']
        if no_of_articles > 100:
            no_of_articles = 100
        
        # Fetching articles based on the number of articles found
        if len(sources) > 20 or len(domains) > 20:
            all_articles = newsapi.get_everything(q=keyword,
                                                  language='en',
                                                  sort_by='relevancy',
                                                  page_size=no_of_articles)['articles']
        else:
            all_articles = newsapi.get_everything(q=keyword,
                                                  sources=sources_str,
                                                  domains=domains_str,
                                                  language='en',
                                                  sort_by='relevancy',
                                                  page_size=no_of_articles)['articles']
        
        return render_template("home.html", all_articles=all_articles, keyword=keyword)
    
    else:
        top_headlines = newsapi.get_top_headlines(country="us", language="en")
        total_results = top_headlines['totalResults']
        if total_results > 100:
            total_results = 100
        all_headlines = newsapi.get_top_headlines(country="us",
                                                  language="en", 
                                                  page_size=total_results)['articles']
        return render_template("home.html", all_headlines=all_headlines)
    
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)

