"""
Service for generating meta descriptions.
"""
from typing import Optional

from .ai_service import generate_content, AIServiceError
from .constants import MAX_DESCRIPTION_LENGTH, MEDICINE_KEYWORDS, DEFAULT_PHARMACY_NAME, DEFAULT_SHOP_NAME, DEFAULT_COMPANY_NAME
from .text_processor import smart_truncate
from .prompt_templates import get_meta_description_prompt, get_paraphrase_prompt


def is_medicine_product(content: str) -> bool:
    """Determine if the content is about a medicine product."""
    return any(keyword in content.lower() for keyword in MEDICINE_KEYWORDS)


def get_company_name(content: str, company_name: str = DEFAULT_COMPANY_NAME) -> str:
    """Get appropriate company name based on content type."""
    # If a custom company name is provided, use it
    if company_name and company_name != DEFAULT_COMPANY_NAME:
        return company_name
    # Otherwise use default pharmacy or shop name based on content
    return DEFAULT_PHARMACY_NAME if is_medicine_product(content) else DEFAULT_SHOP_NAME


def generate_meta_description(content: str, company_name: str = DEFAULT_COMPANY_NAME) -> str:
    """Generate SEO-optimized meta description."""
    if not content:
        return ""
    
    # Create a prompt for generating meta description
    company = get_company_name(content, company_name)
    prompt = get_meta_description_prompt(content, company, MAX_DESCRIPTION_LENGTH)
    
    try:
        description = generate_content(prompt)
        truncated_description = smart_truncate(description, MAX_DESCRIPTION_LENGTH)

        # Ensure description is close to the maximum length
        if len(truncated_description) < MAX_DESCRIPTION_LENGTH:
            # Add supplementary content to extend the description
            extra_content = content[:MAX_DESCRIPTION_LENGTH - len(truncated_description)].strip()
            truncated_description = f"{truncated_description} {extra_content}".strip()
        
        return smart_truncate(truncated_description, MAX_DESCRIPTION_LENGTH)
    except AIServiceError as e:
        # Fallback description without company name
        fallback = f"Find quality products. {content[:MAX_DESCRIPTION_LENGTH - 20]}..."
        return smart_truncate(fallback, MAX_DESCRIPTION_LENGTH)


def paraphrase_description(description: str, company_name: str = DEFAULT_COMPANY_NAME) -> str:
    """Paraphrase existing meta description."""
    if not description:
        return ""
    
    # Create a prompt for paraphrasing the description
    prompt = get_paraphrase_prompt(description, company_name, MAX_DESCRIPTION_LENGTH)
    
    try:
        new_description = generate_content(prompt)
        return smart_truncate(new_description, MAX_DESCRIPTION_LENGTH)
    except AIServiceError as e:
        # Fallback to original description, but remove "at Arogga Online Pharmacy"
        modified = description.replace("at Arogga Online Pharmacy", "")  # Remove company name part
        return smart_truncate(modified, MAX_DESCRIPTION_LENGTH)
