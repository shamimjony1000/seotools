import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import time
import re
import logging
import traceback
import urllib3
import certifi
import warnings

# Suppress only the specific InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    filename='stderr.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_meta_from_url(url: str) -> Optional[Dict[str, str]]:
    """Extract meta tags and content from a given URL."""
    try:
        # Fix malformed URLs
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url.lstrip('://')
        
        logging.info(f"Attempting to fetch URL: {url}")
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Create session with longer timeout and retry strategy
        session = requests.Session()
        session.headers.update(headers)
        
        # Configure retry strategy
        retries = 3
        backoff_factor = 0.5
        
        for attempt in range(retries):
            try:
                # First try with SSL verification
                logging.info(f"Attempt {attempt + 1}/{retries} to fetch URL with SSL verification")
                response = session.get(url, timeout=30, verify=certifi.where())
                response.raise_for_status()
                logging.info("Successfully fetched URL with SSL verification")
                break
            except requests.exceptions.SSLError:
                logging.warning(f"SSL verification failed for {url}, retrying without verification")
                try:
                    response = session.get(url, timeout=30, verify=False)
                    response.raise_for_status()
                    logging.info("Successfully fetched URL without SSL verification")
                    break
                except requests.exceptions.RequestException as e:
                    logging.error(f"Request failed without SSL verification: {str(e)}")
                    if attempt == retries - 1:
                        raise
            except requests.exceptions.ConnectionError as e:
                logging.error(f"Connection Error on attempt {attempt + 1}: {str(e)}")
                if attempt == retries - 1:
                    raise
            except requests.exceptions.Timeout as e:
                logging.error(f"Timeout Error on attempt {attempt + 1}: {str(e)}")
                if attempt == retries - 1:
                    raise
            except requests.exceptions.RequestException as e:
                logging.error(f"Request Error on attempt {attempt + 1}: {str(e)}")
                if attempt == retries - 1:
                    raise
            time.sleep(backoff_factor * (2 ** attempt))
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        description = meta_desc.get('content', '') if meta_desc else ''
        
        # Extract title
        title = soup.title.string if soup.title else ''
        
        # Extract main content
        content_parts = []
        
        # Try multiple selectors for product information
        selectors = [
            ('h1', {}),  # Product name
            ('div', {'class': 'product-details'}),
            ('div', {'class': 'product-description'}),
            ('div', {'class': 'product-info'}),
            ('div', {'id': 'product-info'}),
            ('div', {'class': 'details'}),
            ('div', {'class': 'specifications'})
        ]
        
        for tag, attrs in selectors:
            elements = soup.find_all(tag, attrs)
            for element in elements:
                text = element.get_text(strip=True, separator=' ')
                if text and len(text) > 20:  # Only include substantial content
                    content_parts.append(text)
        
        # Extract structured data if available
        product_schema = soup.find('script', {'type': 'application/ld+json'})
        if product_schema:
            import json
            try:
                schema_data = json.loads(product_schema.string)
                if isinstance(schema_data, dict):
                    if 'description' in schema_data:
                        content_parts.append(schema_data['description'])
                    if 'name' in schema_data:
                        content_parts.insert(0, schema_data['name'])
            except:
                pass
        
        # Combine all content and clean it up
        main_content = ' '.join(content_parts)
        main_content = ' '.join(main_content.split())  # Remove extra whitespace
        
        # If no content was found, use the meta description
        if not main_content and description:
            main_content = description
            
        # Clean up title and description
        title = re.sub(r'\s+', ' ', title).strip()
        description = re.sub(r'\s+', ' ', description).strip()
        main_content = re.sub(r'\s+', ' ', main_content).strip()
        
        return {
            'title': title,
            'description': description,
            'content': main_content
        }
    except Exception as e:
        logging.error(f"Error extracting meta tags: {str(e)}")
        logging.error(traceback.format_exc())
        return None