from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(300), unique=True, nullable=False)
    image_path = db.Column(db.String(300), nullable=True)

db.create_all()
print("Database created")

def save_image(url, article_id):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Create the images directory if it doesn't exist
        if not os.path.exists('images'):
            os.makedirs('images')
        
        image_path = f'images/{article_id}.jpg'
        with open(image_path, 'wb') as file:
            file.write(response.content)
        return image_path
    except Exception as e:
        print(f"Failed to save image: {e}")
        return None

@app.route("/collect_news", methods=['POST'])
def collect_news():
    keyword = request.json.get('keyword')
    sources, domains = get_sources_and_domains()
    
    # Fetching articles based on sources and domains
    if len(sources) > 20 or len(domains) > 20:
        related_news = newsapi.get_everything(q=keyword, language='en', sort_by='relevancy')
    else:
        sources_str = ", ".join(sources)
        domains_str = ", ".join(domains)
        related_news = newsapi.get_everything(q=keyword, sources=sources_str, domains=domains_str, language='en', sort_by='relevancy')
    
    no_of_articles = related_news['totalResults']
    if no_of_articles > 100:
        no_of_articles = 100
    
    all_articles = related_news['articles']
    
    saved_articles = []
    
    for article in all_articles:
        title = article.get('title')
        description = article.get('description')
        url = article.get('url')
        image_url = article.get('urlToImage')
        
        # Check if the article already exists
        existing_article = Article.query.filter_by(url=url).first()
        if existing_article:
            continue
        
        # Save image if it exists
        image_path = save_image(image_url, article_id=len(saved_articles)+1) if image_url else None
        
        # Save the article in the database
        new_article = Article(title=title, description=description, url=url, image_path=image_path)
        
        try:
            db.session.add(new_article)
            db.session.commit()
            saved_articles.append(new_article)
        except IntegrityError:
            db.session.rollback()
            continue
    
    return jsonify({"message": "News collected and stored successfully!", "articles_saved": len(saved_articles)})

if __name__ == "__main__":
    app.run(debug=True)
