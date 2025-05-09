"""
Service for generating SEO keywords from content.
"""
from typing import List

from .ai_service import generate_content, AIServiceError
from .constants import MEDICINE_KEYWORDS, DEFAULT_COMPANY_NAME

def is_medicine_product(content: str) -> bool:
    """Determine if the content is about a medicine product."""
    return any(keyword in content.lower() for keyword in MEDICINE_KEYWORDS)

def generate_keywords(content: str, count: int = 10, company_name: str = DEFAULT_COMPANY_NAME) -> List[str]:
    """
    Generate SEO-optimized keywords from content including company-specific keywords.
    
    Args:
        content (str): The content to generate keywords from
        count (int): Number of keywords to generate (default: 10)
        company_name (str): Company name to include in keywords (default: from constants)
        
    Returns:
        List[str]: List of generated keywords with some company-specific terms
    """
    if not content:
        return []
    
    # Adjust count to be between 5 and 10
    keyword_count = max(5, min(count, 10))
    
    # Create different prompts based on content type
    if is_medicine_product(content):
        prompt = f"""Generate exactly {keyword_count} SEO keywords for a medicine product.
        
        Content: {content}
        
        Rules:
        - Include medicine name, generic name, and purpose
        - Include common search terms for medicine
        - Include symptoms or conditions treated
        - Format as a comma-separated list
        - Each keyword should be 1-4 words long
        - Focus on high search volume terms
        - Include both English and Bangla terms
        - At least 3 keywords MUST include the brand name "{company_name}" (your e-commerce name)
        - Use Bangla medical terms where appropriate
        - Do not include brand names of other medicines
        
        Example output:
        paracetamol, fever medicine, headache relief, {company_name} medicine, {company_name} pharmacy, সর্দি কাশি, মাথা ব্যথা, {company_name} health products, ব্যথা নিবারক
        """
    else:
        prompt = f"""Generate exactly {keyword_count} SEO keywords for this product.
        
        Content: {content}
        
        Rules:
        - Include product type, features, and benefits
        - Include common search terms for this category
        - Format as a comma-separated list
        - Each keyword should be 1-4 words long
        - Focus on high search volume terms
        - Include both English and Bangla terms
        - At least 3 keywords MUST include the brand name "{company_name}" (your e-commerce name)
        - Use Bangla product terms where appropriate
        - Avoid generic terms with high competition
        
        Example output:
        wireless earbuds, bluetooth headphones, noise cancelling, {company_name} earbuds, দীর্ঘস্থায়ী ব্যাটারি, ওয়্যারলেস ইয়ারবাড, {company_name} headphones, ব্লুটুথ হেডফোন, {company_name} electronics
        """
    
    try:
        response = generate_content(prompt)
        # Split by comma and clean up each keyword
        keywords = [keyword.strip() for keyword in response.split(',')]
        
        # Filter out empty keywords and ensure we have the right number
        keywords = [k for k in keywords if k]
        
        # If we have too many keywords, trim the list
        if len(keywords) > keyword_count:
            keywords = keywords[:keyword_count]
            
        # If we have too few keywords, add generic ones to reach minimum count
        if len(keywords) < 5:
            if is_medicine_product(content):
                default_keywords = ["medicine", "pharmacy", "health", "treatment", "online medicine", 
                                   f"{company_name} medicine", f"{company_name} pharmacy", f"{company_name} health products"]
            else:
                default_keywords = ["online shopping", "best price", "quality product", "fast delivery", "discount", 
                                   f"{company_name} shop", f"{company_name} products", f"{company_name} online store"]
                
            keywords.extend(default_keywords[:(5 - len(keywords))])
            
        # Ensure at least one company brand keyword is included
        has_company = any(company_name in kw for kw in keywords)
        if not has_company:
            if is_medicine_product(content):
                keywords.append(f"{company_name} medicine")
            else:
                keywords.append(f"{company_name} products")
            
        return keywords
    except AIServiceError:
        # Fallback to basic keywords with company brand included
        if is_medicine_product(content):
            return ["medicine", "pharmacy", "health", "treatment", "online medicine", 
                   f"{company_name} medicine", f"{company_name} pharmacy"]
        else:
            return ["online shopping", "best price", "quality product", "fast delivery", "discount", 
                   f"{company_name} shop", f"{company_name} products"]
