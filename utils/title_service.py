from .ai_service import generate_content, AIServiceError
from .constants import MEDICINE_KEYWORDS, DEFAULT_PHARMACY_NAME, DEFAULT_SHOP_NAME, DEFAULT_COMPANY_NAME, MAX_TITLE_LENGTH

def extract_medicine_info(content: str) -> tuple:
    """Extract medicine name, strength, and type in both English and Bangla."""
    prompt = f"""Extract medicine information in exact format: "English Name Strength Type|বাংলা নাম স্ট্রেংথ টাইপ"
    Example: "Sergel 20mg Capsule|সারজেল ২০ মি.গ্রা. ক্যাপসুল"
    
    Rules:
    - Keep strength format exact (mg, ml, etc)
    - Preserve medicine type (Capsule, Tablet, etc)
    - Maintain Bangla numerals and units
    - Focus only on medicine name, strength, and type
    - Ensure professional medical terminology
    
    Content: {content}"""
    
    try:
        response = generate_content(prompt)
        names = response.split('|')
        return names[0].strip(), names[1].strip() if len(names) > 1 else ''
    except AIServiceError:
        return content, ""

def is_medicine_product(content: str) -> bool:
    """Determine if the content is about a medicine product."""
    return any(keyword in content.lower() for keyword in MEDICINE_KEYWORDS)

def extract_ecommerce_info(content: str) -> str:
    """Extract product type and key features for non-medicine products."""
    prompt = f"""Extract product information in exact format: "Product Type Key Features"
    Example 1: "Shoes Stylish Summer Exclusive Converse Men"
    Example 2: "Baby Shoes Winter Plush Soft Sole Newborn Baby Girl Princess"
    
    Rules:
    - Keep product type concise (e.g., Shoes, Clothes, etc.)
    - Highlight unique selling points
    - Maintain professional tone
    - Avoid redundancy
    
    Content: {content}"""
    
    try:
        response = generate_content(prompt)
        return response.strip()
    except AIServiceError:
        # Fallback to basic information
        return content[:50] + "..."

def format_medicine_title(name_en: str, name_bn: str, company_name: str = DEFAULT_PHARMACY_NAME) -> str:
    """Format title specifically for medicine products."""
    if name_bn:
        full_title = f"{name_en} and {name_bn} from {company_name}"
    else:
        full_title = f"{name_en} from {company_name}"
    
    if len(full_title) > MAX_TITLE_LENGTH:
        available_length = MAX_TITLE_LENGTH - len(f" from {company_name}")
        if name_bn:
            parts = f"{name_en} and {name_bn}"
            truncated = parts[:available_length].rsplit(' and ', 1)[0]
        else:
            truncated = name_en[:available_length]
        return f"{truncated} from {company_name}"
    
    return full_title

def format_regular_title(title: str, company_name: str = DEFAULT_SHOP_NAME) -> str:
    """Format title for non-medicine products."""
    full_title = f"{title} available at {company_name}"
    if len(full_title) > MAX_TITLE_LENGTH:
        available_length = MAX_TITLE_LENGTH - len(f" available at {company_name}")
        truncated = title[:available_length]
        return f"{truncated} available at {company_name}"
    return full_title

def generate_title(content: str, company_name: str = DEFAULT_COMPANY_NAME) -> str:
    """Generate SEO-optimized title with proper formatting."""
    try:
        if is_medicine_product(content):
            name_en, name_bn = extract_medicine_info(content)
            return format_medicine_title(name_en, name_bn, company_name)
        else:
            ecommerce_info = extract_ecommerce_info(content)
            return format_regular_title(ecommerce_info, company_name)
            
    except AIServiceError:
        # Fallback to a basic title if AI service fails
        return format_regular_title(content[:50] + "...", company_name)
