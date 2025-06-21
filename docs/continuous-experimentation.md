# Continuous Experimentation: Sentiment Analysis Model Comparison

## Experiment Overview

We are conducting an A/B test to compare two versions of our sentiment analysis system. The experiment aims to evaluate whether our new model version (v2) and enhanced application features provide better accuracy and user satisfaction compared to the current version (v1).

### Base Design vs. New Design

**Base Design (v1)**:
- Uses sentiment analysis model version `v0.1.5`
- Basic application with standard sentiment analysis
- Simple feedback collection
- Standard confidence display

**New Design (v2)**:
- Uses sentiment analysis model version `v0.1.4` (different model version for comparison)
- Enhanced application with feedback experiment features
- Advanced feedback collection with unique review IDs
- Detailed confidence level descriptions
- User satisfaction tracking
- Enhanced user experience with descriptive messages

## Hypothesis

Our falsifiable hypothesis is that the new system version (v2) will:
1. Provide more accurate sentiment predictions (measured through user feedback)
2. Increase user engagement through enhanced feedback collection
3. Improve user satisfaction scores
4. Maintain or improve response times
5. Show better feedback submission rates

## Metrics and Decision Process

We are collecting the following metrics through Prometheus and visualizing them in Grafana:

1. **Positive Sentiment Ratio by Version**
   - Tracks the ratio of positive to total predictions for each version
   - Helps identify if one version is biased towards positive/negative predictions
   - Expected: v2 should show a more balanced ratio closer to historical data

2. **Model Response Time**
   - Measures the latency of sentiment predictions
   - Critical for user experience
   - Requirement: v2 should not increase average response time by more than 10%

3. **Sentiment Predictions by Version**
   - Shows the distribution of predictions (positive/negative) for each version
   - Helps identify potential biases or shifts in prediction patterns
   - Expected: v2 should maintain a reasonable distribution based on domain knowledge

4. **User Feedback Metrics**
   - **Feedback Submission Rate**: Percentage of reviews that receive user feedback
   - **User Satisfaction Score**: Average satisfaction based on feedback correctness
   - **Model Accuracy**: Based on user feedback (correct/incorrect predictions)
   - Success Criteria: v2 should show at least 20% improvement in feedback submission rate

5. **Model Version Comparison**
   - **v1 Model**: Uses `v0.1.5` model version
   - **v2 Model**: Uses `v0.1.4` model version
   - Compare accuracy between different model versions

## Decision Making Process

The experiment will run for a minimum of 2 weeks, with traffic split 90/10 between versions (90% v1, 10% v2). The decision to adopt v2 will be based on:

1. **Primary Metrics**: 
   - User-reported accuracy: Must show statistically significant improvement (p < 0.05)
   - Feedback submission rate: Must show at least 20% improvement over v1
   - User satisfaction score: Must be higher than v1 baseline

2. **Secondary Metrics**:
   - Response time: Must not degrade by more than 10%
   - Sentiment ratio: Should be within ±10% of historical baseline
   - No significant increase in error rates or failures

3. **Monitoring Process**:
   - Daily review of Grafana dashboard metrics
   - Weekly statistical significance testing
   - Continuous monitoring of system health and error rates

## Implementation Details

The experiment is implemented using:
- **Istio for traffic splitting** (based on request header `x-user-experiment`)
- **Prometheus for metrics collection**
- **Grafana for visualization and monitoring**
- **Custom metrics in our application code**
- **Versioned model releases** from GitHub releases

### Traffic Splitting Configuration
```yaml
traffic:
  abTesting:
    enabled: true
    matchHeader: x-user-experiment
    controlValue: A
    experimentValue: B
    appVersions:
      - v1
      - v2
    modelVersions:
      - v1
      - v2
```

### Model Versioning
- **v1 Model**: Uses `TRAINED_MODEL_VERSION=v0.1.5`
- **v2 Model**: Uses `TRAINED_MODEL_VERSION=v0.1.4`
- Models are downloaded from GitHub releases using version tags
- Each model version is cached separately in `/mnt/shared`

### Application Versions
- **v1 App**: Standard sentiment analysis application
- **v2 App**: Enhanced application with feedback experiment features
  - Unique review ID generation
  - Enhanced feedback collection
  - User satisfaction tracking
  - Detailed confidence level descriptions

### Metrics Implementation
- Application-level metrics for sentiment analysis
- Response time tracking
- User feedback collection with correctness tracking
- Error rate monitoring
- User satisfaction score calculation

## Dashboard Visualization

Our Grafana dashboard (search for "Sentiment Analysis A/B Testing") provides real-time visualization of:
- Sentiment prediction distributions by version
- Response time comparisons
- User feedback metrics and submission rates
- Model accuracy based on user feedback
- Error rates and system health

The dashboard shows:
- **Top Left**: Positive Sentiment Ratio by Version - tracking the proportion of positive predictions
- **Top Right**: Model Response Time - monitoring latency and performance
- **Bottom Left**: Sentiment Predictions by Version - showing the distribution of predictions
- **Bottom Right**: User Feedback Metrics - displaying feedback submission rates and satisfaction scores

## Technical Implementation

### Model Service Updates
- **New Version-Based Approach**: Uses `TRAINED_MODEL_VERSION` instead of `ARTIFACT_ID`
- **GitHub Releases**: Models are downloaded from versioned GitHub releases
- **A/B Testing Support**: Multiple model versions can run simultaneously
- **Enhanced Feedback**: Improved feedback collection and storage

### Application Updates
- **v2 Features**: Enhanced feedback collection, user satisfaction tracking
- **New Endpoints**: `/api/feedback/stats` for experiment metrics
- **Enhanced Metrics**: Additional Prometheus metrics for A/B testing
- **Variant Identification**: API responses include variant information

### Deployment Updates
- **Multiple Deployments**: Separate deployments for v1 and v2 versions
- **Istio Routing**: Header-based traffic splitting
- **Service Mesh**: Destination rules for version subsets
- **Monitoring**: Enhanced metrics collection and visualization

## Rollback Plan

If any of the following conditions are met, we will immediately rollback to v1:
1. Error rate increases by more than 5%
2. Response time degrades by more than 20%
3. User satisfaction score drops below v1 baseline
4. Critical bugs or security issues are discovered

## Results and Conclusions

[To be filled after the experiment completion]

## Next Steps

1. **Deploy the updated A/B testing configuration**
2. **Monitor initial metrics and system health**
3. **Collect baseline data for 1 week**
4. **Begin experiment with 10% traffic to v2**
5. **Daily monitoring and weekly analysis**
6. **Statistical significance testing after 2 weeks**
7. **Decision on full rollout or rollback** 