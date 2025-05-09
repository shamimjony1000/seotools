import google.generativeai as genai
from dotenv import load_dotenv
import os
from typing import Optional

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key="AIzaSyA8k5-cC2WGEbgo6S-zuxPNcj8MmxBiVkU")

class AIServiceError(Exception):
    """Custom exception for AI service errors."""
    pass

def validate_response(response) -> bool:
    """Validate if the response is safe and appropriate."""
    if not hasattr(response, 'text') or not response.text:
        return False
    return True

def generate_content(prompt: str, max_retries: int = 3) -> str:
    """
    Generate content using Gemini Pro model with improved error handling.
    
    Args:
        prompt (str): The prompt to generate content from
        max_retries (int): Maximum number of retry attempts
        
    Returns:
        str: Generated content
        
    Raises:
        AIServiceError: If content generation fails after all retries
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    generation_config = {
        'temperature': 0.5,
        'top_p':0.94,
        'max_output_tokens': 1024,
    }
    
    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
    }
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            if validate_response(response):
                return response.text.strip()
                
            # If response is not valid, try modifying the prompt
            modified_prompt = f"""Generate safe and appropriate content for:
            
            {prompt}
            
            Requirements:
            - Keep content professional and factual
            - Avoid any potentially harmful or dangerous content
            - Focus on product information and benefits"""
            
            response = model.generate_content(
                modified_prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            if validate_response(response):
                return response.text.strip()
                
        except Exception as e:
            if attempt == max_retries - 1:
                raise AIServiceError(f"Failed to generate content: {str(e)}")
            continue
            
    raise AIServiceError("Failed to generate appropriate content after multiple attempts")
