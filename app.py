# Import necessary libraries
from flask import Flask, render_template, request
from newsapi import NewsApiClient

# Initialize the Flask web application
app = Flask(__name__)

# Initialize the News API client with a specific API key for authentication
newsapi = NewsApiClient(api_key='c7ceb304f7de46b091b25f6096a1e515')

# Define a helper function to extract sources and domains from News API
def get_sources_and_domains():
    # Retrieve a list of all news sources available from the News API
    all_sources = newsapi.get_sources()['sources']
    
    # Initialize empty lists to store source IDs and domain names
    sources = []
    domains = []

    # Iterate through each source in the retrieved list
    for e in all_sources:
        id = e['id']  # Extract the source ID
        domain = e['url']  # Extract the source URL
        
        # Clean the domain by removing URL prefixes
        domain = domain.replace("http://", "")  # Remove "http://" prefix
        domain = domain.replace("https://", "")  # Remove "https://" prefix
        domain = domain.replace("www.", "")  # Remove "www." prefix
        
        # Remove any path after the domain name (if present)
        slash = domain.find('/')  # Find the position of '/' in the domain
        if slash != -1:
            domain = domain[:slash]  # Trim the domain to remove the path
        
        # Add the cleaned domain and source ID to the respective lists
        sources.append(id)
        domains.append(domain)
    
    # Return the lists of source IDs and domain names
    return sources, domains

# Define a route for the home page that handles both GET and POST requests
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        # When the form is submitted (POST request)
        sources, domains = get_sources_and_domains()  # Get the available sources and domains
        keyword = request.form["keyword"]  # Retrieve the search keyword entered by the user
        
        # Check if the number of sources or domains is large
        if len(sources) > 20 or len(domains) > 20:
            # If there are too many sources or domains, make a request without specifying them
            related_news = newsapi.get_everything(q=keyword,
                                                  language='en',
                                                  sort_by='relevancy')
        else:
            # Convert the lists of sources and domains to comma-separated strings
            sources_str = ", ".join(sources)
            domains_str = ", ".join(domains)
            # Make a request to get news articles based on the specified sources and domains
            related_news = newsapi.get_everything(q=keyword,
                                                  sources=sources_str,
                                                  domains=domains_str,
                                                  language='en',
                                                  sort_by='relevancy')
        
        # Retrieve the total number of articles available for the given keyword
        no_of_articles = related_news['totalResults']
        if no_of_articles > 20:
            no_of_articles = 20  # Limit the number of articles to a maximum of 20
        
        # Fetch the actual articles based on the number of articles available
        if len(sources) > 20 or len(domains) > 20:
            # If there are too many sources or domains, make a request with a limited number of articles
            all_articles = newsapi.get_everything(q=keyword,
                                                  language='en',
                                                  sort_by='relevancy',
                                                  page_size=no_of_articles)['articles']
        else:
            # Make a request to get articles based on specified sources and domains, with a limited number of articles
            all_articles = newsapi.get_everything(q=keyword,
                                                  sources=sources_str,
                                                  domains=domains_str,
                                                  language='en',
                                                  sort_by='relevancy',
                                                  page_size=no_of_articles)['articles']
        
        # Render the home page template with the retrieved articles and the search keyword
        return render_template("home.html", all_articles=all_articles, keyword=keyword)
    
    else:
        # When the page is accessed via a GET request (initial page load)
        # Fetch top headlines from the News API for the US
        top_headlines = newsapi.get_top_headlines(country="us", language="en")
        
        # Retrieve the total number of top headlines available
        total_results = top_headlines['totalResults']
        if total_results > 20:
            total_results = 20  # Limit the number of headlines to a maximum of 100
        
        # Fetch the top headlines with a limited number of results
        all_headlines = newsapi.get_top_headlines(country="us",
                                                  language="en", 
                                                  page_size=total_results)['articles']
        
        # Render the home page template with the top headlines
        return render_template("home.html", all_headlines=all_headlines)
    
    # Fallback to render home page template if no conditions match (should not reach this point)
    return render_template("home.html")

# Run the Flask web application with debugging enabled, allowing for real-time error tracking
if __name__ == "__main__":
    app.run(debug=True)
