from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils.description_service import generate_meta_description, paraphrase_description
from utils.title_service import generate_title
from utils.url_service import extract_meta_from_url
from utils.keyword_service import generate_keywords
from utils.product_description_service import generate_product_description
from utils.constants import DEFAULT_COMPANY_NAME
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze-url', methods=['POST', 'OPTIONS'])
def analyze_url():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.json
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Extract metadata from URL
        meta_data = extract_meta_from_url(url)
        if not meta_data:
            return jsonify({'error': 'Failed to extract metadata from URL'}), 400

        # Get company name from request or use default
        company_name = data.get('company_name', DEFAULT_COMPANY_NAME)
        
        # Generate title, description, and keywords
        generated_title = generate_title(meta_data['content'], company_name)
        generated_description = generate_meta_description(meta_data['content'], company_name)
        generated_keywords = generate_keywords(meta_data['content'], company_name=company_name)

        return jsonify({
            'original_title': meta_data['title'],
            'original_description': meta_data.get('description', ''),
            'original_content': meta_data['content'],
            'generated_title': generated_title,
            'generated_description': generated_description,
            'generated_keywords': generated_keywords
        })
    except Exception as e:
        app.logger.error(f"Error in analyze_url: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    try:
        data = request.json
        content = data.get('content')
        if not content:
            return jsonify({'error': 'Content is required'}), 400

        # Get company name from request or use default
        company_name = data.get('company_name', DEFAULT_COMPANY_NAME)
        
        # Generate title, description, and keywords
        generated_title = generate_title(content, company_name)
        generated_description = generate_meta_description(content, company_name)
        generated_keywords = generate_keywords(content, company_name=company_name)

        return jsonify({
            'generated_title': generated_title,
            'generated_description': generated_description,
            'generated_keywords': generated_keywords
        })
    except Exception as e:
        app.logger.error(f"Error in generate_content: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/paraphrase', methods=['POST'])
def paraphrase():
    try:
        data = request.json
        text = data.get('text')
        if not text:
            return jsonify({'error': 'Text is required'}), 400

        # Get company name from request or use default
        company_name = data.get('company_name', DEFAULT_COMPANY_NAME)
        
        # Generate paraphrased text
        paraphrased_text = paraphrase_description(text, company_name)

        return jsonify({
            'paraphrased_text': paraphrased_text
        })
    except Exception as e:
        app.logger.error(f"Error in paraphrase: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/product-description', methods=['POST'])
def product_description():
    try:
        data = request.json
        product_info = data.get('product_info')
        if not product_info:
            return jsonify({'error': 'Product information is required'}), 400

        # Get company name from request or use default
        company_name = data.get('company_name', DEFAULT_COMPANY_NAME)
        
        # Generate product description
        product_description = generate_product_description(product_info, company_name)

        return jsonify({
            'product_description': product_description
        })
    except Exception as e:
        app.logger.error(f"Error in product_description: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000, threaded=True)
