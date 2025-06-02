# Continuous Experimentation: Feedback Button Position

## Experiment Overview

This experiment tests the hypothesis that placing feedback buttons closer to the sentiment analysis result will increase user engagement with the feedback system.

### Base Design (v1)
- Feedback buttons are placed below the sentiment result
- Users need to scroll down to provide feedback
- Clear separation between result and feedback sections

### Experimental Design (v2)
- Feedback buttons are placed directly next to the sentiment result
- Compact "Correct?" prompt instead of "Was this analysis correct?"
- Visual indicators (✓ and ✗) added to feedback buttons
- Color-coded buttons (green for yes, red for no)

## Hypothesis

**Primary Hypothesis**: Moving feedback buttons closer to the sentiment result and making them more visually appealing will increase the feedback submission rate by at least 20%.

### Supporting Hypotheses:
1. Users will submit feedback more quickly due to reduced cognitive load
2. The feedback accuracy (correlation between model prediction and user feedback) will remain consistent between versions

## Metrics

The following metrics are collected to evaluate the experiment:

1. **Feedback Submission Rate**
   - Metric: `feedback_submissions_total`
   - Type: Counter
   - Purpose: Track total number of feedback submissions per version

2. **Time to Feedback**
   - Metric: `feedback_timing_seconds`
   - Type: Histogram
   - Buckets: [1s, 5s, 10s, 30s, 60s, 120s]
   - Purpose: Measure how quickly users provide feedback after seeing results

3. **Feedback Accuracy**
   - Metric: `feedback_accuracy_total{accuracy="correct|incorrect"}`
   - Type: Counter with labels
   - Purpose: Monitor if the UI change affects agreement between model and users

## Decision Process

### Data Collection
- Both versions will run simultaneously using Istio traffic splitting
- Users are randomly assigned to versions using the `x-user-experiment` header
- Data will be collected for a minimum of 2 weeks or 1000 reviews per version

### Success Criteria
The experiment will be considered successful if:
1. Feedback submission rate increases by ≥20% in v2
2. Median time to feedback decreases by ≥25% in v2
3. Feedback accuracy remains within ±5% between versions

### Grafana Dashboard
The experiment is monitored through a dedicated Grafana dashboard that shows:
1. Feedback submission rates comparison (v1 vs v2)
2. Time to feedback distribution
3. Feedback accuracy rates
4. Total reviews and feedback counts

[Dashboard Screenshot to be added after deployment]

### Rollout Plan
1. Deploy v2 to 50% of users
2. Monitor metrics for 2 weeks
3. If success criteria are met:
   - Roll out v2 to 100% of users
   - Document learnings
4. If criteria are not met:
   - Analyze failure points
   - Consider alternative designs
   - Roll back to v1

## Technical Implementation

### Version Control
- v1: Current implementation in main branch
- v2: Experimental implementation in `feature/feedback-position` branch

### Traffic Management
Using Istio for traffic splitting:
- 50% traffic to v1 (control)
- 50% traffic to v2 (experiment)
- Split based on `x-user-experiment` header

### Monitoring
- Prometheus metrics exposed via `/metrics` endpoint
- Custom metrics added for experiment tracking
- Grafana dashboard for real-time monitoring

## Current Status

[To be updated during the experiment] 