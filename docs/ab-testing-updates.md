# A/B Testing Implementation Updates

## Overview

This document summarizes the changes needed to update the A/B testing implementation from the old artifact-based approach to the new version-based approach, and to add the missing app v2 implementation.

## Key Changes Made

### 1. Model Service Updates

#### Old Approach (Artifact-Based)
- Used `ARTIFACT_ID` environment variable
- Downloaded models from GitHub artifacts using artifact IDs
- Hardcoded artifact ID: `"3219218428"`
- Environment variables: `VECT_FILE_NAME_IN_ZIP`, `MODEL_FILE_NAME_IN_ZIP`

#### New Approach (Version-Based)
- Uses `TRAINED_MODEL_VERSION` environment variable
- Downloads models from GitHub releases using version tags
- Supports multiple model versions for A/B testing
- Environment variables: `VECT_FILE_NAME`, `MODEL_FILE_NAME`

### 2. Model Deployment Template Updates

**File**: `operation/sentiment-analysis/templates/deployment-models.yml`

**Changes**:
- Added A/B testing support with multiple model versions
- Updated environment variables to use new naming convention
- Added version labels for Istio routing
- Replaced `ARTIFACT_ID` with `TRAINED_MODEL_VERSION`
- Updated file name references

### 3. Values Configuration Updates

**File**: `operation/sentiment-analysis/values.yaml`

**Changes**:
- Removed `artifactId` field
- Added `version` field for single deployment
- Added `versions` map for A/B testing
- Updated model image to latest version (`v0.1.6-rc.1`)
- Updated environment variable names
- Added model version mapping for v1 and v2

### 4. App v2 Implementation

**New Files Created**:
- `app/backend-v2/app.py` - Enhanced application with feedback experiment features
- `app/Dockerfile-v2` - Dockerfile for v2 app
- `app/VERSION-v2` - Version file for v2 app
- `app/README-v2.md` - Documentation for v2 features

**Key v2 Features**:
- Unique review ID generation for feedback tracking
- Enhanced feedback collection with satisfaction scoring
- Detailed confidence level descriptions
- New `/api/feedback/stats` endpoint for A/B testing metrics
- Enhanced user experience with descriptive messages
- Additional Prometheus metrics for experiment tracking

### 5. Documentation Updates

**File**: `operation/docs/continuous-experimentation.md`

**Changes**:
- Updated experiment overview to reflect new implementation
- Added technical implementation details
- Updated metrics and decision process
- Added model versioning information
- Updated deployment and monitoring sections

## Deployment Configuration

### Current A/B Testing Setup

```yaml
# values.yaml
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

model:
  images:
    v1: ghcr.io/remla25-team14/model-service:v0.1.6-rc.1
    v2: ghcr.io/remla25-team14/model-service:v0.1.6-rc.1
  versions:
    v1: "v0.1.5"
    v2: "v0.1.4"

app:
  images:
    v1: ghcr.io/remla25-team14/app/app:sha-06d792c
    v2: ghcr.io/remla25-team14/app/app:v2-feedback-experiment
```

### Traffic Splitting

- **90% traffic to v1** (control group)
- **10% traffic to v2** (experiment group)
- Header-based routing: `x-user-experiment: B` for v2
- Consistent user experience throughout session

## Model Versioning

### Version-Based Model Loading

The new model service supports loading different model versions:

```python
# model-service/app.py
TRAINED_MODEL_VERSION = os.getenv("TRAINED_MODEL_VERSION", "v0.1.0")

# Models are downloaded from GitHub releases
def download_from_github_release(version, asset_name, dest_path):
    url = f"https://github.com/{REPO}/releases/download/{version}/{asset_name}"
```

### Model Cache Structure

```
/mnt/shared/
├── v0.1.4/
│   ├── c1_BoW_Sentiment_Model.pkl
│   └── c2_Classifier_v1.pkl
└── v0.1.5/
    ├── c1_BoW_Sentiment_Model.pkl
    └── c2_Classifier_v1.pkl
```

## Metrics and Monitoring

### New Metrics in v2 App

- `feedback_submissions_total` - Counter for feedback submissions by correctness
- `user_satisfaction_score` - Gauge for average user satisfaction
- Enhanced sentiment tracking with review IDs

### Grafana Dashboard

The "Sentiment Analysis A/B Testing" dashboard shows:
- Sentiment prediction distributions by version
- Response time comparisons
- User feedback metrics and submission rates
- Model accuracy based on user feedback

## Next Steps

### 1. Build and Deploy v2 App

```bash
# Build v2 app image
cd app
docker build -f Dockerfile-v2 -t ghcr.io/remla25-team14/app/app:v2-feedback-experiment .

# Push to registry
docker push ghcr.io/remla25-team14/app/app:v2-feedback-experiment
```

### 2. Deploy Updated Configuration

```bash
# Deploy the updated Helm chart
cd operation/sentiment-analysis
helm upgrade sentiment . --values values.yaml
```

### 3. Verify Deployment

```bash
# Check deployments
kubectl get deployments -l app=sentiment-app
kubectl get deployments -l app=sentiment-model

# Check services
kubectl get services -l app=sentiment-app
kubectl get services -l app=sentiment-model

# Test traffic splitting
curl -H "x-user-experiment: A" http://sentiment.local/api/version
curl -H "x-user-experiment: B" http://sentiment.local/api/version
```

### 4. Monitor Experiment

- Check Grafana dashboard for metrics
- Monitor application logs for feedback collection
- Track user satisfaction scores
- Analyze feedback submission rates

## Rollback Plan

If issues arise:

1. **Disable A/B testing**: Set `traffic.abTesting.enabled: false` in values.yaml
2. **Revert to single version**: All traffic will go to v1
3. **Monitor system health**: Ensure stability before re-enabling

## Benefits of New Implementation

1. **Version-Based Model Management**: Easier to manage and deploy different model versions
2. **Enhanced A/B Testing**: Proper support for both app and model version testing
3. **Better Feedback Collection**: Comprehensive feedback tracking for experiment evaluation
4. **Improved Monitoring**: Enhanced metrics for statistical analysis
5. **GitHub Release Integration**: Models are versioned and released through GitHub releases
6. **Scalable Architecture**: Easy to add more versions or experiments in the future 