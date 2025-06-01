# Continuous Experimentation: Review Length Warning Feature

## Experiment Overview
This experiment tests whether displaying a warning message for reviews shorter than 10 words will increase the average review length by at least 20%. The hypothesis is based on the assumption that providing immediate feedback to users about review length will encourage them to write more detailed reviews.

## Base Design vs. New Feature

### Base Design (Control Version)
- Users can submit reviews of any length
- No feedback is provided about review length
- Reviews are processed directly for sentiment analysis

### New Feature (Experimental Version)
- Users receive a warning message when attempting to submit reviews shorter than 10 words
- The warning includes:
  - Current word count
  - Minimum required word count
  - Encouraging message to write a more detailed review
- Reviews meeting the length requirement proceed to sentiment analysis

## Hypothesis
**Hypothesis**: Displaying a warning for reviews shorter than 10 words will increase the average review length by at least 20%.

This hypothesis is falsifiable through:
1. Measuring average review lengths in both versions
2. Calculating the percentage difference
3. Comparing against the 20% target increase

## Implementation Details

### Deployment Strategy
We have deployed two versions of the sentiment analysis service:
1. **Control Version**: Original implementation without warnings
2. **Experimental Version**: Implementation with the review length warning feature

Both versions are deployed simultaneously using Kubernetes, with traffic split between them through a LoadBalancer service.

### Technical Implementation
1. **Backend Changes**:
   - Added word count functionality
   - Implemented warning system for short reviews
   - Added new metrics for experiment tracking
   - Version-specific behavior controlled by environment variables

2. **Frontend Changes**:
   - Added warning message display
   - Enhanced UI to show current word count
   - Version information display
   - Improved error handling

3. **Metrics Implementation**:
   ```python
   # Experiment-specific metrics
   review_length_total = Counter('review_length_total', 'Total number of words in reviews', ['version'])
   review_count_total = Counter('review_count_total', 'Total number of reviews submitted', ['version'])
   short_review_warnings_total = Counter('short_review_warnings_total', 'Number of short review warnings shown')
   ```

## Metrics and Monitoring

### Key Metrics
1. **Average Review Length**: 
   - Calculated per version (control vs. experimental)
   - Formula: `review_length_total / review_count_total`
   - Tracked over time to observe trends

2. **Warning Display Rate**:
   - Frequency of warning messages shown
   - Helps understand how often users encounter the feature

3. **Review Submission Rate**:
   - Monitors if the warning affects user engagement
   - Ensures the feature doesn't discourage users from submitting reviews

### Grafana Dashboard
We have created a dedicated Grafana dashboard (available in `grafana-experiment.json`) that visualizes:
1. Average review length comparison between versions
2. Warning display frequency
3. Review submission rates for both versions

[Screenshot will be added once the experiment is running]

## Decision Process

### Data Collection
The experiment will run for two weeks, collecting the following data:
1. Average review lengths for both versions
2. Number of reviews submitted in each version
3. Frequency of warning displays
4. User engagement metrics (submission rates)

### Success Criteria
The experiment will be considered successful if:
1. **Primary Metric**: The experimental version shows an average review length at least 20% higher than the control version
2. **Secondary Metric**: The review submission rate in the experimental version remains within 10% of the control version

### Analysis Process
1. **Daily Monitoring**:
   - Track average review lengths
   - Monitor submission rates
   - Check for any unexpected patterns

2. **Weekly Analysis**:
   - Calculate rolling averages
   - Assess statistical significance
   - Review user engagement metrics

3. **Final Decision**:
   - Compare two-week averages
   - Verify statistical significance
   - Check secondary metrics
   - Make deployment decision

### Decision Making
The final decision will be based on:
1. **Primary Goal**: ≥20% increase in average review length
2. **Secondary Considerations**:
   - User engagement (submission rates)
   - Warning effectiveness (response to warnings)
   - Overall user experience

If the experiment meets the success criteria, the feature will be rolled out to all users. If not, we will either:
1. Adjust the warning threshold
2. Modify the warning message
3. Explore alternative approaches to encourage longer reviews

## Current Status
The experiment is currently being implemented. This document will be updated with results, screenshots, and the final decision once the experiment concludes. 