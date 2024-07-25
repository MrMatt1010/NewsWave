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
# The code here allows the user to select the region they want to read the news from via the drop down menu in the html
@app.route("/", methods=['GET', 'POST'])
def home():
  if request.method == "POST":
    region = request.form.get("region")  # Get the selected region
    keyword = request.form["keyword"]
    
    if region:
      top_headlines = newsapi.get_top_headlines(country=region, language="en")
    else:
      # Default to New Zealand if no region selected
      top_headlines = newsapi.get_top_headlines(country="nz", language="en")
    
    total_results = top_headlines['totalResults']
    if total_results > 100:
      total_results = 100
    all_headlines = newsapi.get_top_headlines(country=region,  # Use selected region
                                              language="en", 
                                              page_size=total_results)['articles']
    return render_template("home.html", all_headlines=all_headlines, keyword=keyword)
  
  else:
    # Display initial page with default region (NZ)
    top_headlines = newsapi.get_top_headlines(country="nz", language="en")
    total_results = top_headlines['totalResults']
    if total_results > 100:
      total_results = 100
    all_headlines = newsapi.get_top_headlines(country="nz", language="en", page_size=total_results)['articles']
    return render_template("home.html", all_headlines=all_headlines)
  
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)

