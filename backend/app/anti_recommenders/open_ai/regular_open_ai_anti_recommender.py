import logging
from typing import Tuple
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser

from .open_ai_anti_recommender import OpenAIAntiRecommender


class RegularOpenAIAntiRecommender(OpenAIAntiRecommender):
    """A subclass of the OpenAI Anti-Recommender"""
    
    def build_model(self):
        """Build and return an LLM"""
        
        try:
            model = OpenAI()
            prompt = PromptTemplate.from_template(super().get_template())

            chain = (
                {"question": RunnablePassthrough()}
                    | prompt
                    | model
                    | StrOutputParser()
            )

            return chain
        
        except Exception:
            super().get_logger().warning("error while building the OpenAI chain.", exc_info=True)

            return 1

       

    def generate_response(self, query: str, chain) -> str:
        """Generate response from LLM"""
        
        response = ""

        try:
            response = chain.invoke(query)
        
        except Exception:
            super().get_logger().warning("error while generating response from the OpenAI chain.", exc_info=True)

        return response
        
    
    def parse_response(self, response: str) -> Tuple[Tuple, ...]:
        """Extract alternate articles from the LLMs and return a list of anti-recommendations"""
        
        response_list = response.strip().split('\n')
        alternate_articles = []

        for line in response_list:
            line_chunk = line.split("-")
        
            if len(line_chunk) < 2:
                continue
        
            title = line_chunk[1].strip()

            url = ""
            if "wikipedia" in line_chunk[-1]:
                url = line_chunk[-1].strip()
                
            alternate_articles.append((title, url))
    
        return tuple(alternate_articles)
    

    def generate_anti_recommendations(self, wikipedia_title : str) -> Tuple[Tuple, ...]:
        """Returns a tuple of anti-recommendations for the given wikipedia title"""

        chain = self.build_model()
        
        query = self.create_query(wikipedia_title)
 
        response = self.generate_response(query, chain)
 
        parsed_response = self.parse_response(response)

        return parsed_response