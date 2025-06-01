from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from libversion import VersionUtil
import os
import requests
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Initialize metrics
metrics = PrometheusMetrics(app, path=None)
metrics.info('app_info', 'Application info', version=VersionUtil.get_version())

# Experiment metrics
review_length_total = Counter('review_length_total', 'Total number of words in reviews', ['version'])
review_count_total = Counter('review_count_total', 'Total number of reviews submitted', ['version'])
short_review_warnings_total = Counter('short_review_warnings_total', 'Number of short review warnings shown')

# Original metrics
sentiment_ratio = Gauge('sentiment_ratio', 'Ratio of positive to total reviews')
sentiment_predictions = Counter('sentiment_predictions_total', 'Number of sentiment predictions', ['sentiment'])
model_response_time = Histogram('model_response_time_seconds', 'Model service response time in seconds', 
                               buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0])

# Configuration
MODEL_SERVICE_URL = os.environ.get('MODEL_SERVICE_URL', 'http://localhost:5000')
APP_VERSION = os.environ.get('APP_VERSION', 'unknown')
EXPERIMENT_VERSION = os.environ.get('EXPERIMENT_VERSION', 'control')
ENABLE_SHORT_REVIEW_WARNING = os.environ.get('ENABLE_SHORT_REVIEW_WARNING', 'false').lower() == 'true'
MIN_REVIEW_WORDS = 10

def count_words(text):
    """Count the number of words in a text."""
    return len(text.split())

@app.route('/metrics')
def metrics_endpoint():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/version', methods=['GET'])
@metrics.counter('api_calls_version', 'Number of calls to version endpoint')
def version():
    model_version = 'unavailable'
    try:
        response = requests.get(f"{MODEL_SERVICE_URL}/version", timeout=5)
        if response.status_code == 200:
            model_version = response.json().get('model_version', 'unknown')
    except requests.RequestException:
        pass
    
    return jsonify({
        "app": {
            "app_version": APP_VERSION,
            "experiment_version": EXPERIMENT_VERSION
        },
        "model_service": {
            "model_version": model_version
        }
    })

@app.route('/api/analyze', methods=['POST'])
@metrics.counter('api_calls_analyze', 'Number of calls to analyze endpoint')
def analyze_sentiment():
    data = request.json
    
    if not data or 'review' not in data:
        return jsonify({"error": "Missing review text"}), 400
    
    review = data['review']
    word_count = count_words(review)
    
    # Update experiment metrics
    review_length_total.labels(version=EXPERIMENT_VERSION).inc(word_count)
    review_count_total.labels(version=EXPERIMENT_VERSION).inc()
    
    # Check for short review in experimental version
    if ENABLE_SHORT_REVIEW_WARNING and word_count < MIN_REVIEW_WORDS:
        short_review_warnings_total.inc()
        return jsonify({
            "warning": f"Your review is too short. Please write at least {MIN_REVIEW_WORDS} words for a more meaningful review.",
            "word_count": word_count,
            "min_required": MIN_REVIEW_WORDS
        }), 400
    
    # Track model service response time
    start_time = time.time()
    
    try:
        # Forward the request to the model service
        response = requests.post(
            f"{MODEL_SERVICE_URL}/analyze",
            json={"review": review},
            timeout=10
        )
        
        # Record response time
        response_time = time.time() - start_time
        model_response_time.observe(response_time)
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Track sentiment prediction
            sentiment_value = response_data.get('sentiment')
            sentiment_label = 'positive' if sentiment_value is True else 'negative'
            sentiment_predictions.labels(sentiment=sentiment_label).inc()
            
            # Update sentiment ratio
            if sentiment_value is True:
                sentiment_ratio.inc()
            
            if sentiment_value is True:
                response_data['emoji'] = '😊'  
            else:
                response_data['emoji'] = '😔' 
            if 'confidence' not in response_data:
                response_data['confidence'] = None
                
            return jsonify(response_data)
        else:
            return jsonify({"error": f"Model service error: {response.status_code}"}), 500
    except requests.RequestException as e:
        # Record response time for failed requests too
        response_time = time.time() - start_time
        model_response_time.observe(response_time)
        return jsonify({"error": f"Failed to connect to model service: {str(e)}"}), 503

@app.route('/api/feedback', methods=['POST'])
@metrics.counter('api_calls_feedback', 'Number of calls to feedback endpoint')
def submit_feedback():
    data = request.json
    
    if not data or 'review_id' not in data or 'correct_sentiment' not in data:
        return jsonify({"error": "Missing review_id or correct_sentiment"}), 400
        
    return jsonify({
        "status": "success",
        "message": "Feedback received"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 