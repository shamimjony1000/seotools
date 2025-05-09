"""
Service for generating product descriptions.
"""
from typing import Dict, Tuple
import re

from .ai_service import generate_content, AIServiceError
from .constants import MEDICINE_KEYWORDS, DEFAULT_COMPANY_NAME

def is_medicine_product(content: str) -> bool:
    """Determine if the content is about a medicine product."""
    return any(keyword in content.lower() for keyword in MEDICINE_KEYWORDS)


def is_bengali_text(text: str) -> bool:
    """Determine if the text contains Bengali characters."""
    # Bengali Unicode range: \u0980-\u09FF
    bengali_pattern = re.compile(r'[\u0980-\u09FF]')
    # If at least 15% of the text contains Bengali characters, consider it Bengali
    bengali_chars = len(re.findall(bengali_pattern, text))
    return bengali_chars > 0 and bengali_chars / len(text) > 0.15 if text else False

def generate_product_description(product_info: str, company_name: str = DEFAULT_COMPANY_NAME) -> Dict[str, str]:
    """
    Generate a beautiful product description from basic product information.
    Automatically detects if input is in Bengali and provides output in Bengali.
    
    Args:
        product_info (str): Basic information about the product
        
    Returns:
        Dict[str, str]: Dictionary containing different sections of the product description
    """
    if not product_info:
        return {
            "short_description": "",
            "long_description": "",
            "features": [],
            "benefits": []
        }
    
    # Determine if this is a medicine product and if the text is in Bengali
    is_medicine = is_medicine_product(product_info)
    is_bengali = is_bengali_text(product_info)
    
    # Create a prompt for generating the product description
    if is_medicine and is_bengali:
        prompt = f"""Generate a beautiful, SEO-friendly product description for a medicine product in Bengali (Bangla) language.

Product Information: {product_info}

Please format your response in the following JSON structure:
{{
  "short_description": "A compelling 1-2 sentence summary of the product in Bengali",
  "long_description": "A detailed 3-5 paragraph description highlighting key benefits, uses, and unique selling points in Bengali",
  "features": ["Feature 1 in Bengali", "Feature 2 in Bengali", "Feature 3 in Bengali", "Feature 4 in Bengali", "Feature 5 in Bengali"],
  "benefits": ["Benefit 1 in Bengali", "Benefit 2 in Bengali", "Benefit 3 in Bengali", "Benefit 4 in Bengali"]
}}

Guidelines:
- Write ENTIRELY in Bengali language
- Highlight medical benefits and uses
- Include appropriate dosage information if available
- Mention quality and effectiveness
- Focus on quality healthcare
- Use medical terminology appropriately
- Ensure the content is factual and ethical
- Do not make unsubstantiated medical claims
"""
    elif is_bengali:
        prompt = f"""Generate a beautiful, SEO-friendly product description for an e-commerce product in Bengali (Bangla) language.

Product Information: {product_info}

Please format your response in the following JSON structure:
{{
  "short_description": "A compelling 1-2 sentence summary of the product in Bengali",
  "long_description": "A detailed 3-5 paragraph description highlighting key benefits, features, and unique selling points in Bengali",
  "features": ["Feature 1 in Bengali", "Feature 2 in Bengali", "Feature 3 in Bengali", "Feature 4 in Bengali", "Feature 5 in Bengali"],
  "benefits": ["Benefit 1 in Bengali", "Benefit 2 in Bengali", "Benefit 3 in Bengali", "Benefit 4 in Bengali"]
}}

Guidelines:
- Write ENTIRELY in Bengali language
- Highlight product quality and uniqueness
- Emphasize key features and benefits
- Use persuasive language to encourage purchase
- Target both emotional and practical buyer motivations
- Make the description vivid and engaging
"""    
    else:
        prompt = f"""Generate a beautiful, SEO-friendly product description for an e-commerce product.

Product Information: {product_info}

Please format your response in the following JSON structure:
{{
  "short_description": "A compelling 1-2 sentence summary of the product",
  "long_description": "A detailed 3-5 paragraph description highlighting key benefits, features, and unique selling points",
  "features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5"],
  "benefits": ["Benefit 1", "Benefit 2", "Benefit 3", "Benefit 4"]
}}

Guidelines:
- Highlight product quality and uniqueness
- Emphasize key features and benefits
- Use persuasive language to encourage purchase
- Target both emotional and practical buyer motivations
- Use Bangla terms where appropriate
- Make the description vivid and engaging
"""
    
    try:
        response = generate_content(prompt)
        
        # First, try to clean up the response to ensure it's valid JSON
        cleaned_response = response
        # Try to find JSON content if it's wrapped in other text
        if '{' in response and '}' in response:
            start_idx = response.find('{')
            end_idx = response.rfind('}')
            if start_idx >= 0 and end_idx >= 0:
                cleaned_response = response[start_idx:end_idx+1]
        
        # Parse the JSON response
        import json
        import re
        try:
            # Try to parse the cleaned response as JSON
            description_data = json.loads(cleaned_response)
            
            # Ensure all expected keys are present
            result = {
                "short_description": description_data.get("short_description", ""),
                "long_description": description_data.get("long_description", ""),
                "features": description_data.get("features", []),
                "benefits": description_data.get("benefits", [])
            }
            
            return result
        except json.JSONDecodeError:
            # If JSON parsing fails, extract sections using regex
            # This is more robust than string finding
            short_desc = ""
            long_desc = ""
            features = []
            benefits = []
            
            # Extract short description
            short_desc_match = re.search(r'"short_description"\s*:\s*"([^"]+)"', response)
            if short_desc_match:
                short_desc = short_desc_match.group(1).strip()
            
            # Extract long description
            long_desc_match = re.search(r'"long_description"\s*:\s*"([^"]+)"', response)
            if long_desc_match:
                long_desc = long_desc_match.group(1).strip()
            # If regex didn't work, try a more lenient approach for multiline descriptions
            if not long_desc and '"long_description"' in response:
                try:
                    parts = response.split('"long_description"')[1].split('"features"')[0]
                    long_desc = parts.split('"')[1].strip()
                except:
                    pass
            
            # Extract features
            features_match = re.findall(r'"features"\s*:\s*\[([^\]]+)\]', response)
            if features_match:
                feature_items = re.findall(r'"([^"]+)"', features_match[0])
                features = [item.strip() for item in feature_items]
            
            # Extract benefits
            benefits_match = re.findall(r'"benefits"\s*:\s*\[([^\]]+)\]', response)
            if benefits_match:
                benefit_items = re.findall(r'"([^"]+)"', benefits_match[0])
                benefits = [item.strip() for item in benefit_items]
            
            # If we still don't have descriptions, try to extract from plain text
            if not short_desc and 'short description' in response.lower():
                lines = response.split('\n')
                for i, line in enumerate(lines):
                    if 'short description' in line.lower() and i+1 < len(lines):
                        short_desc = lines[i+1].strip()
                        break
            
            if not long_desc and 'detailed description' in response.lower():
                lines = response.split('\n')
                for i, line in enumerate(lines):
                    if 'detailed description' in line.lower() and i+1 < len(lines):
                        # Try to capture multiple lines
                        long_desc_lines = []
                        j = i+1
                        while j < len(lines) and 'features' not in lines[j].lower() and 'benefits' not in lines[j].lower():
                            long_desc_lines.append(lines[j].strip())
                            j += 1
                        long_desc = ' '.join(long_desc_lines)
                        break
            
            # Ensure we have at least some content
            if not short_desc and not long_desc and features and benefits:
                short_desc = "Premium quality product with exceptional features."
                long_desc = "This exceptional product combines quality, functionality, and style. Perfect for your needs."
            
            return {
                "short_description": short_desc,
                "long_description": long_desc,
                "features": features,
                "benefits": benefits
            }
            
    except AIServiceError:
        # Fallback description
        if is_medicine and is_bengali:
            return {
                "short_description": "উচ্চ-মানের ঔষধ যা কার্যকরী চিকিৎসার জন্য।",
                "long_description": "এই প্রিমিয়াম ঔষধটি কার্যকরী উপশম প্রদানের জন্য ডিজাইন করা হয়েছে। এটি উচ্চ-মানের উপাদান দিয়ে তৈরি যা নিরাপত্তা এবং কার্যকারিতার সর্বোচ্চ মান পূরণ করে।",
                "features": ["মানসম্পন্ন উপাদান", "কার্যকরী ফর্মুলা", "বিশ্বস্ত ফর্মুলেশন", "মেডিকেল-গ্রেড মান", "প্রতিযোগিতামূলক মূল্য"],
                "benefits": ["দ্রুত উপশম", "ব্যবহার করা সহজ", "নির্ভরযোগ্য ফলাফল", "গ্রাহক সন্তুষ্টি"]
            }
        elif is_medicine:
            return {
                "short_description": "High-quality medicine product for effective treatment.",
                "long_description": "This premium medicine product is designed to provide effective relief. It is formulated with high-quality ingredients that meet the highest standards of safety and efficacy.",
                "features": ["Quality ingredients", "Effective formula", "Trusted formulation", "Medical-grade quality", "Competitive price"],
                "benefits": ["Fast relief", "Easy to use", "Reliable results", "Customer satisfaction"]
            }
        elif is_bengali:
            return {
                "short_description": "অসাধারণ বৈশিষ্ট্য সহ প্রিমিয়াম মানের পণ্য।",
                "long_description": "এই অসাধারণ পণ্যটি মান, কার্যকারিতা এবং স্টাইল একত্রিত করে। এটি সেরা অভিজ্ঞতা প্রদান এবং উন্নত কর্মক্ষমতা ও ডিজাইনের মাধ্যমে আপনার প্রত্যাশা ছাড়িয়ে যাওয়ার জন্য ডিজাইন করা হয়েছে।",
                "features": ["উচ্চ মান", "টেকসই ডিজাইন", "প্রিমিয়াম উপাদান", "চমৎকার কারিগরি", "উন্নত ফিনিশ"],
                "benefits": ["দীর্ঘস্থায়ী কর্মক্ষমতা", "অর্থের জন্য দুর্দান্ত মূল্য", "গ্রাহক সন্তুষ্টি", "ব্যবহারিক এবং স্টাইলিশ"]
            }
        else:
            return {
                "short_description": "Premium quality product with exceptional features.",
                "long_description": "This exceptional product combines quality, functionality, and style. It is designed to provide the best experience and exceed your expectations with superior performance and design.",
                "features": ["High quality", "Durable design", "Premium materials", "Excellent craftsmanship", "Superior finish"],
                "benefits": ["Long-lasting performance", "Great value for money", "Customer satisfaction", "Practical and stylish"]
            }
