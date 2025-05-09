# Templates for AI Prompt Generation

def get_meta_description_prompt(content: str, company_name: str, max_length: int) -> str:
    """Generate a prompt for SEO-optimized meta description."""
    return f"""
Generate an SEO-optimized meta description for this product:
"{content}"

Requirements:
1. Use EXACTLY this format: "Get [Product Name] ([বাংলা নাম]) at [Benefits...]"
2. Skip Words: 'Daraz', 'Aroggga.com', 'Arogga', 'Daraz.com.bd', 'MedEx', 'Medex.com', 'Medex.com.bd','MedEasy'
3. Keep ALL Bangla (বাংলা) words exactly as written.
4. Include specific benefits and uses.
5. Maintain a minimum of {max_length} characters.
6. End with a complete sentence.
7. Use NO line breaks or special formatting.
8. Focus on key product features and benefits.
9. Make it compelling and informative.
10. Always include "{company_name}".
11. Do NOT copy input words directly.
12. Ensure a minimum of 160 characters.
"""

def get_paraphrase_prompt(description: str, company_name: str, max_length: int) -> str:
    """Generate a prompt for paraphrasing a product description."""
    return f"""
Paraphrase this description:
"{description}"

Requirements:
1. Use EXACTLY this format: "Get [Product] ([বাংলা নাম]) at [Benefits...]"
2. Skip Words: 'Daraz', 'Aroggga.com', 'Arogga', 'Daraz.com.bd', 'MedEx', 'Medex.com', 'Medex.com.bd','MedEasy'
3. Keep ALL Bangla (বাংলা) words exactly as written.
4. Include ALL key benefits and features.
5. Maintain a minimum of {max_length} characters.
6. End with a complete sentence.
7. Use NO line breaks or special formatting.
8. Make it unique while maintaining key information.
9. Ensure natural flow and readability.
10. Always include "{company_name}".
11. Do NOT copy input words directly.
12. Ensure a minimum of 160 characters.
"""

# Example usage
if __name__ == "__main__":
    content_example = "Best quality headphones with superior sound and comfort."
    description_example = "These headphones offer premium sound quality and ergonomic design."

    company_name = "Example Company"
    max_length = 160

    # Generate meta description prompt
    meta_description_prompt = get_meta_description_prompt(content_example, company_name, max_length)
    print("Meta Description Prompt:")
    print(meta_description_prompt)

    # Generate paraphrase prompt
    paraphrase_prompt = get_paraphrase_prompt(description_example, company_name, max_length)
    print("\nParaphrase Prompt:")
    print(paraphrase_prompt)
