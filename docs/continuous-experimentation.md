# Continuous Experimentation: Sentiment Analysis Threshold Optimization

## Experiment Overview
This document describes a continuous experiment to optimize the sentiment analysis threshold in our application.

### Base Design
The current sentiment analysis service uses a default threshold of 0.5 to classify reviews as positive or negative. When the model's confidence score is above this threshold, the review is classified as positive; otherwise, it's classified as negative.

### Proposed Change
We will test a higher threshold (0.7) to determine if it leads to more accurate sentiment predictions from the user's perspective. The hypothesis is that by requiring a higher confidence score to classify a review as positive, we may reduce false positives and increase user satisfaction.

### Hypothesis
**Hypothesis**: "Using a higher sentiment threshold (0.7) instead of the default (0.5) leads to higher user satisfaction with sentiment predictions as measured by explicit user feedback."

This hypothesis is falsifiable through:
1. User feedback accuracy metrics
2. Confidence score distribution analysis
3. Classification distribution changes

## Technical Implementation

### Service Versions
- **Control (v1)**: 
  - Sentiment threshold: 0.5 (default)
  - Traffic: Users with no header or `x-user-experiment: A`
- **Experiment (v2)**:
  - Sentiment threshold: 0.7
  - Traffic: Users with header `x-user-experiment: B`

### Traffic Management
Traffic splitting is implemented using Istio's traffic management features:
- Users are split based on the `x-user-experiment` header
- Control group: Header value 'A' or no header
- Experiment group: Header value 'B'

### Metrics Collection
The following metrics are collected for both versions:

1. **Classification Counts**:
   - `sentiment_positive_classifications_total{threshold="0.5|0.7"}`
   - `sentiment_negative_classifications_total{threshold="0.5|0.7"}`

2. **Confidence Scores**:
   - `sentiment_confidence_scores{threshold="0.5|0.7"}`
   - Provides histogram of confidence scores for analysis

3. **User Feedback**:
   - `sentiment_precision_feedback{threshold="0.5|0.7",correct="true|false"}`
   - Direct measure of prediction accuracy based on user feedback

## Decision Process

### Data Collection
1. The experiment will run for 15 minutes to gather quick test data
2. Both versions will receive traffic through the header-based routing
3. Metrics are collected in Prometheus and visualized in Grafana in real-time

### Quick Test Plan
1. Send at least 10 reviews to each version:
   ```bash
   # Control version (0.5 threshold)
   curl -H "Host: sentiment.local" http://localhost/analyze -d '{"review": "test"}'
   
   # Experiment version (0.7 threshold)
   curl -H "Host: sentiment.local" -H "x-user-experiment: B" http://localhost/analyze -d '{"review": "test"}'
   ```

2. For each review, submit feedback about correctness:
   ```bash
   curl -H "Host: sentiment.local" http://localhost/feedback -d '{"review_id": "<ID>", "correct_sentiment": true/false}'
   ```

### Success Metrics
Primary metrics for quick testing:

1. **User Feedback Accuracy Rate**:
   ```
   sum(sentiment_precision_feedback{correct="true"}) by (threshold) /
   sum(sentiment_precision_feedback) by (threshold)
   ```
   - Higher is better
   - Looking for clear trend differences between versions

2. **Confidence Score Distribution**:
   - Analysis of the confidence score histogram
   - Understanding if the higher threshold affects the distribution of predictions

3. **Classification Balance**:
   ```
   sum(sentiment_positive_classifications_total) by (threshold) /
   (sum(sentiment_positive_classifications_total) by (threshold) + 
    sum(sentiment_negative_classifications_total) by (threshold))
   ```
   - Monitor for extreme imbalances in classifications

### Decision Criteria
For this quick test, the experiment will be considered successful if:

1. The feedback accuracy rate for threshold 0.7 shows better results in the 15-minute test period
2. The classification balance remains within reasonable bounds (20-80% positive)
3. No errors or issues are observed during testing

### Monitoring Dashboard
A dedicated Grafana dashboard will be used to monitor in real-time:
1. Accuracy rates for both versions
2. Classification distributions
3. Confidence score distributions
4. User feedback rates

### Rollback Plan
If any of the following occurs during the 15-minute test, immediately rollback to the 0.5 threshold:
1. Any drop in user feedback accuracy
2. Extreme imbalance in classifications
3. System errors or performance issues

## Results
(To be filled after the quick test)

### Metrics Summary
TBD

### Decision
TBD

### Lessons Learned
TBD 