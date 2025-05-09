import requests
import json

def test_url_analysis():
    url = "http://localhost:5000/api/analyze-url"
    data = {
        "url": "https://www.arogga.com/product/7569/fexomin-120-tablet-120mg?pv_id=7569"
    }
    
    response = requests.post(url, json=data)
    print("\nURL Analysis Test:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_generate_content():
    url = "http://localhost:5000/api/generate-content"
    data = {
        "content": "Fexomin 120mg Tablet is an antihistamine medication used to treat allergies."
    }
    
    response = requests.post(url, json=data)
    print("\nContent Generation Test:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_paraphrase():
    url = "http://localhost:5000/api/paraphrase"
    data = {
        "text": "Fexomin 120mg Tablet provides quick relief from allergy symptoms."
    }
    
    response = requests.post(url, json=data)
    print("\nParaphrase Test:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_url_analysis()
    test_generate_content()
    test_paraphrase()
