# SEO Tools

![SEO Tools Banner](https://img.shields.io/badge/SEO-Tools-blue?style=for-the-badge)

A comprehensive suite of SEO tools designed to optimize your web content for better search engine rankings and user engagement.

## 🚀 Features

- **URL Analysis**: Extract and analyze metadata from any URL
- **Title Generation**: Create SEO-optimized titles for your content
- **Meta Description Generation**: Generate compelling meta descriptions
- **Keyword Generation**: Identify relevant keywords for your content
- **Content Paraphrasing**: Rewrite content while maintaining context and meaning
- **Product Description Generation**: Create engaging product descriptions

## 📋 Requirements

- Python 3.6+
- Flask
- Flask-CORS
- Google Generative AI
- BeautifulSoup4
- Requests
- Python-dotenv

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shamimjony1000/seotools.git
   cd seotools
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with your API keys and configuration.

## 🚀 Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Access the web interface at `http://localhost:5000`

3. Use the API endpoints:
   - `/api/analyze-url`: Analyze content from a URL
   - `/api/generate-content`: Generate SEO content from text
   - `/api/paraphrase`: Paraphrase existing content
   - `/api/product-description`: Generate product descriptions

## 🔧 API Endpoints

### Analyze URL
```
POST /api/analyze-url
```
Request body:
```json
{
  "url": "https://example.com",
  "company_name": "Your Company"
}
```

### Generate Content
```
POST /api/generate-content
```
Request body:
```json
{
  "content": "Your content here",
  "company_name": "Your Company"
}
```

### Paraphrase Text
```
POST /api/paraphrase
```
Request body:
```json
{
  "text": "Text to paraphrase",
  "company_name": "Your Company"
}
```

### Generate Product Description
```
POST /api/product-description
```
Request body:
```json
{
  "product_info": "Product details here",
  "company_name": "Your Company"
}
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Developer

Developed by **Shamim MD Jony**

---

© 2025 SEO Tools. All rights reserved.
