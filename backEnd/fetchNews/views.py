from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from newsapi import NewsApiClient
from .models import Article
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt

# Initialize the News API client
newsapi = NewsApiClient(api_key='cad07dc33d534c508a93ae9128e9d716')

# Helper function to get sources and domains
def get_sources_and_domains():
    all_sources = newsapi.get_sources()['sources']
    sources = []
    domains = []
    for e in all_sources:
        id = e['id']
        domain = e['url'].replace("http://", "").replace("https://", "").replace("www.", "")
        slash = domain.find('/')
        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)
    return sources, domains

# Django view for fetching and storing news articles
@csrf_exempt
def fetch_and_store_articles(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword", "")
        sources, domains = get_sources_and_domains()

        # Fetch related news articles
        if len(sources) > 20 or len(domains) > 20:
            related_news = newsapi.get_everything(q=keyword, language='en', sort_by='relevancy')
        else:
            sources_str = ", ".join(sources)
            domains_str = ", ".join(domains)
            related_news = newsapi.get_everything(q=keyword, sources=sources_str, domains=domains_str, language='en', sort_by='relevancy')

        no_of_articles = min(related_news['totalResults'], 100)
        articles = related_news['articles'][:no_of_articles]

        # Store articles in the database
        stored_articles = []
        for article in articles:
            article_obj, created = Article.objects.get_or_create(
                title=article['title'],
                url=article['url'],
                defaults={
                    'description': article.get('description', ''),
                    'published_at': parse_datetime(article['publishedAt']),
                    'source_name': article['source']['name'],
                }
            )
            if created:
                stored_articles.append(article_obj)

        # Return the stored articles as JSON
        return JsonResponse({
            "message": f"{len(stored_articles)} articles fetched and stored successfully.",
            "articles": list(Article.objects.values())
        }, safe=False)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

# Endpoint testing
def test_endpoint(request):
    return JsonResponse({"message": "Endpoint Reached."}, status=200)