from openai import OpenAI
import google.generativeai as genai
from config import Config
from googlesearch import search
from gnews import GNews
import requests
from bs4 import BeautifulSoup
import json

class LLMService:
    def __init__(self):
        self.ai_provider = Config.AI_PROVIDER
        if self.ai_provider == 'openai':
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        else:  # gemini
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        
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
        Verify if a given text is likely true or false using the configured AI provider.
        """
        try:
            # Get search results and news articles
            search_results = self.get_google_search_results(text)
            news_results = self.get_news_articles(text)

            # Create a comprehensive prompt
            prompt = """
            Analyze this statement and determine if it's true or false.
            Statement: "{text}"
            
            Search Results: {search_results}
            News Articles: {news_results}
            
            Provide a fact-check response in valid JSON format with these exact fields:
            {{
                "verdict": "TRUE/FALSE/UNCERTAIN",
                "confidence": 85,
                "explanation": "Your detailed explanation here",
                "sources": [
                    {{
                        "url": "source URL",
                        "relevance": "relevance explanation"
                    }}
                ],
                "recent_developments": "recent updates",
                "potential_biases": ["bias 1", "bias 2"],
                "fact_check_date": "current date"
            }}
            
            Important: Ensure the response is valid JSON and all strings are properly escaped.
            """.format(
                text=text,
                search_results=json.dumps(search_results),
                news_results=json.dumps(news_results)
            )

            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a fact-checking AI. Respond only with valid JSON."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                result = response.choices[0].message.content
            else:  # gemini
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.2
                    )
                )
                result = response.text

            # Clean and parse the response
            try:
                # Remove any markdown formatting that might be present
                result = result.replace("```json", "").replace("```", "").strip()
                verification_result = json.loads(result)
            except json.JSONDecodeError as e:
                return {
                    "verdict": "ERROR",
                    "confidence": 0,
                    "explanation": f"Failed to parse AI response: {str(e)}",
                    "sources": [],
                    "recent_developments": "Error in response format",
                    "potential_biases": [],
                    "fact_check_date": "",
                    "search_results": search_results,
                    "news_articles": news_results
                }
            
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