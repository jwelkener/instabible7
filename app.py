import os
import requests
from flask import Flask, request, send_file, jsonify, render_template

app = Flask(__name__)

# Replace with your Unsplash API access key
UNSPLASH_ACCESS_KEY = 'RYeAAvMeSnOwSekAFq2XwYY4H8IDjUbbZVSVFzOO0ik'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search-images', methods=['GET'])
def search_images():
    query = request.args.get('query')
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    # Unsplash API URL for image search
    url = 'https://api.unsplash.com/search/photos'
    params = {
        'query': query,
        'client_id': UNSPLASH_ACCESS_KEY,
        'per_page': 10,  # Number of images to return
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch images from Unsplash'}), response.status_code
    
    data = response.json()

    # Extract URLs for each image result
    image_urls = [result['urls']['regular'] for result in data['results']]

    return jsonify({'images': image_urls})

def download_image(image_url, filename='downloaded_image.jpg'):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        return filename
    return None


@app.route('/download-image', methods=['GET'])
def download_image_route():
    search_query = request.args.get('query')
    if not search_query:
        return jsonify({'error': 'Query parameter is required'}), 400

    # Unsplash API endpoint
    url = 'https://api.unsplash.com/search/photos'
    params = {
        'query': search_query,
        'client_id': UNSPLASH_ACCESS_KEY,
        'per_page': 1,  # Download only one image for now
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch image from Unsplash'}), response.status_code

    data = response.json()

    if len(data['results']) == 0:
        return jsonify({'error': 'No images found for the search term'}), 404

    image_url = data['results'][0]['urls']['regular']

    # Download the image
    filename = download_image(image_url)

    if filename:
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({'error': 'Failed to download image'}), 500

if __name__ == '__main__':
    app.run(debug=True)
