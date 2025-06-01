import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [review, setReview] = useState('');
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [warning, setWarning] = useState(null);
  const [versions, setVersions] = useState({ app: null, model: null, experiment: null });
  
  useEffect(() => {
    async function fetchVersions() {
      try {
        const response = await fetch('/api/version');
        const data = await response.json();
        
        setVersions({
          app: data.app.app_version,
          model: data.model_service.model_version,
          experiment: data.app.experiment_version
        });
      } catch (err) {
        console.error('Failed to fetch versions:', err);
        setVersions({
          app: 'Error fetching',
          model: 'Error fetching',
          experiment: 'Error fetching'
        });
      }
    }
    
    fetchVersions();
  }, []);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!review.trim()) {
      setError('Please enter a review');
      return;
    }
    
    setLoading(true);
    setError(null);
    setWarning(null);
    setSentiment(null);
    
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ review }),
      });
      
      const data = await response.json();
      
      if (response.status === 400 && data.warning) {
        setWarning(data);
        setLoading(false);
        return;
      }
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to analyze sentiment');
      }
      
      setSentiment(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const submitFeedback = async (isCorrect) => {
    if (!sentiment || !sentiment.review_id) return;
    
    try {
      await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          review_id: sentiment.review_id,
          correct_sentiment: isCorrect ? sentiment.sentiment : !sentiment.sentiment
        }),
      });
      
      alert('Thank you for your feedback!');
    } catch (err) {
      console.error('Failed to submit feedback:', err);
    }
  };
  
  return (
    <div className="App">
      <header>
        <h1>Restaurant Review Sentiment Analysis</h1>
        <div className="version-info">
          <p>App Version: {versions.app || 'Loading...'}</p>
          <p>Model Version: {versions.model || 'Loading...'}</p>
          <p>Experiment Version: {versions.experiment || 'Loading...'}</p>
        </div>
      </header>
      
      <main>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="review">Enter your restaurant review:</label>
            <textarea
              id="review"
              value={review}
              onChange={(e) => setReview(e.target.value)}
              placeholder="The food was amazing and the service was excellent!"
              rows={4}
            />
            {warning && (
              <div className="warning">
                <p>{warning.warning}</p>
                <p>Current word count: {warning.word_count}</p>
              </div>
            )}
          </div>
          
          <button type="submit" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Sentiment'}
          </button>
          
          {error && <div className="error">{error}</div>}
        </form>
        
        {sentiment && (
          <div className="result">
            <h2>Analysis Result</h2>
            <div className="sentiment">
              <p>{sentiment.sentiment ? '😊 Positive' : '😞 Negative'}</p>
              {sentiment.confidence && (
                <p>Confidence: {(sentiment.confidence * 100).toFixed(0)}%</p>
              )}
            </div>
            
            <div className="feedback">
              <p>Was this analysis correct?</p>
              <div>
                <button onClick={() => submitFeedback(true)}>Yes</button>
                <button onClick={() => submitFeedback(false)}>No</button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App; 