import streamlit as st

def count_characters(text: str) -> int:
    """Count the number of characters in the given text."""
    return len(text)

def display_box_style(title: str, description: str):
    """Display meta information in box style and show character counts."""
    
    # Count the characters in title and description
    title_char_count = count_characters(title)
    description_char_count = count_characters(description)
    
    st.markdown("""
        <style>
        .meta-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd;
            margin-bottom: 20px;
        }
        .meta-label {
            color: #666;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .meta-content {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #e9ecef;
            font-family: monospace;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="meta-box">
            <div class="meta-label">Title (80 characters max)</div>
            <div class="meta-content">{title}</div>
            <div class="meta-content">Character count: {title_char_count}</div>
        </div>
        <div class="meta-box">
            <div class="meta-label">Description (160 characters)</div>
            <div class="meta-content">{description}</div>
            <div class="meta-content">Character count: {description_char_count}</div>
        </div>
    """, unsafe_allow_html=True)
