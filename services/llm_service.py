from openai import OpenAI
from config import Config
from googlesearch import search
from gnews import GNews
import requests
from bs4 import BeautifulSoup
import json

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.google_news = GNews(language='en', country='US', period='7d', max_results=5)

    def get_google_search_results(self, query: str, num_results: int = 5) -> list:
        """Get relevant search results from Google."""
        try:
            search_results = []
            for url in search(query, num_results=num_results):
                try:
                    response = requests.get(url, timeout=5)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.string if soup.title else "No title"
                    search_results.append({
                        "title": title,
                        "url": url
                    })
                except Exception:
                    continue
            return search_results
        except Exception as e:
            return [{"error": str(e)}]

    def get_news_articles(self, query: str) -> list:
        """Get relevant news articles from Google News."""
        try:
            news_results = self.google_news.get_news(query)
            return [
                {
                    "title": article["title"],
                    "url": article["url"],
                    "published": article["published date"],
                    "source": article["publisher"]["title"]
                }
                for article in news_results
            ]
        except Exception as e:
            return [{"error": str(e)}]

    def verify_fact(self, text: str) -> dict:
        """
        Verify if a given text is likely true or false using GPT-3.5 and web sources.
        Returns a dictionary with the verdict and explanation.
        """
        try:
            # Get search results and news articles
            search_results = self.get_google_search_results(text)
            news_results = self.get_news_articles(text)

            # Create a comprehensive prompt with the search results
            prompt = f"""
            Please analyze the following statement and determine if it's likely true or false.
            Use the provided search results and news articles for verification.
            
            Statement: "{text}"
            
            Recent Google Search Results:
            {json.dumps(search_results, indent=2)}
            
            Recent News Articles:
            {json.dumps(news_results, indent=2)}
            
            Based on the above sources and your knowledge, provide a comprehensive fact-check.
            
            Respond in the following JSON format:
            {{
                "verdict": "TRUE/FALSE/UNCERTAIN",
                "confidence": "percentage (0-100)",
                "explanation": "detailed explanation",
                "sources": [
                    {{
                        "url": "source URL",
                        "relevance": "how this source supports the verdict"
                    }}
                ],
                "recent_developments": "any recent news or updates related to this topic",
                "potential_biases": ["any potential biases identified"],
                "fact_check_date": "current date and time"
            }}
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a fact-checking AI assistant focused on accuracy and truth verification. Use provided sources to verify claims."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            # Extract the content from the response
            result = response.choices[0].message.content
            verification_result = eval(result)
            
            # Add source materials to the result
            verification_result["search_results"] = search_results
            verification_result["news_articles"] = news_results
            
            return verification_result

        except Exception as e:
            return {
                "verdict": "ERROR",
                "confidence": 0,
                "explanation": f"Error during verification: {str(e)}",
                "sources": [],
                "recent_developments": "Unable to fetch recent developments",
                "potential_biases": [],
                "fact_check_date": "",
                "search_results": [],
                "news_articles": []
            } 