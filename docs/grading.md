# Grading Rubrics

## A1: Versions, Releases, and Containerization

### Automated Release Process
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | Artifacts not versioned/released; libraries on public repos (e.g., Maven Central)                                                     |       |
| Poor         | All artifacts released but not automated                                                                                              |       |
| Sufficient   | All artifacts versioned + released via workflows                                                                                      |       |
| Good         | Auto-versioning via Git tags; pre-release version bumps                                                                               |       |
| Excellent    | Multi-arch images; multi-stage Dockerfiles; pre-release version formats                                                               |       |

### Software Reuse in Libraries
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | Libraries not included as dependencies                                                                                                |       |
| Poor         | Partial library reuse via package manager                                                                                             |       |
| Sufficient   | Both libs reused as external dependencies                                                                                              |       |
| Good         | Meaningful logic reuse; consistent preprocessing; auto-versioning                                                                     |       |
| Excellent    | Model decoupled from container; cache-enabled downloads                                                                               |       |

### Exposing a Model via REST
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | Non-REST communication used                                                                                                           |       |
| Poor         | Broken component communication                                                                                                        |       |
| Sufficient   | REST used consistently; Flask for model serving                                                                                       |       |
| Good         | Configurable model-service URL; OpenAPI docs                                                                                          |       |
| Excellent    | Configurable model-service port                                                                                                       |       |

### Docker Compose Operation
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | No `docker-compose.yml`                                                                                                               |       |
| Poor         | Startup fails; incorrect service exposure                                                                                             |       |
| Sufficient   | Working Docker Compose setup; app-service accessible                                                                                  |       |
| Good         | Volume/port mappings; env vars; same images as K8s                                                                                    |       |
| Excellent    | Restart policies; Docker secrets; env files                                                                                           |       |

---

## A2: Provisioning a Kubernetes Cluster

### Setting up (Virtual) Infrastructure
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | VMs missing/broken                                                                                                                    |       |
| Poor         | Vagrantfile errors; provisioning failures                                                                                             |       |
| Sufficient   | All VMs operational; private network; host-reachable; Ansible provisioning ≤5min                                                      |       |
| Good         | Loops/templates for nodes; variable-controlled resources                                                                              |       |
| Excellent    | Ansible args passed; valid inventory.cfg                                                                                              |       |

### Setting up Software Environment
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | Playbooks trivial/provisioning fails                                                                                                  |       |
| Poor         | Non-trivial playbooks exist                                                                                                           |       |
| Sufficient   | Installs packages/starts services/copies files/edits configs                                                                          |       |
| Good         | Idempotent tasks; shared variables; loops; no cluster re-initialization                                                               |       |
| Excellent    | Dynamic `/etc/hosts`; waiting steps; idempotent regex replacements                                                                    |       |

### Setting up Kubernetes
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | Nodes unregistered; `kubectl` inaccessible                                                                                            |       |
| Poor         | Cluster runs but workloads fail                                                                                                       |       |
| Sufficient   | Working `kubectl` config; in-class exercises deployable                                                                               |       |
| Good         | LoadBalancer (MetalLB); Ingress Controller (Nginx); Istio Gateway                                                                     |       |
| Excellent    | Dashboard accessible; fixed IPs for Ingress/Istio; HTTPS Ingress                                                                      |       |

---

## A3: Operate and Monitor Kubernetes

### Kubernetes Usage
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | Missing core resources (Deployment/Service)                                                                                           |       |
| Poor         | Accessible only via NodePort/tunnel                                                                                                   |       |
| Sufficient   | Deployable to K8s; Ingress access; Deployment+Service defined                                                                         |       |
| Good         | Configurable model-service location; ConfigMap/Secret usage                                                                           |       |
| Excellent    | Shared VirtualBox volume mounted via `hostPath`                                                                                       |       |

### Helm Installation
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | No/trivial Helm chart                                                                                                                 |       |
| Poor         | Chart incomplete/installation fails                                                                                                   |       |
| Sufficient   | Complete deployment chart                                                                                                             |       |
| Good         | Customizable via `values.xml` (e.g., service name)                                                                                    |       |
| Excellent    | Supports multiple installations in same cluster                                                                                       |       |

### App Monitoring
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | <3 metrics; Prometheus collection fails                                                                                               |       |
| Poor         | Missing Gauge/Counter examples                                                                                                        |       |
| Sufficient   | 3+ app-specific metrics; includes Gauge+Counter; Prometheus auto-discovers                                                           |       |
| Good         | Histogram metric; metrics broken down by labels                                                                                       |       |
| Excellent    | AlertManager + non-trivial PrometheusRule; no credentials in files                                                                    |       |

### Grafana
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | No/trivial dashboard                                                                                                                  |       |
| Poor         | Dashboard incomplete/import errors                                                                                                    |       |
| Sufficient   | Basic dashboard; manual import via JSON; installation docs                                                                            |       |
| Good         | Visualizations for Gauges/Counters; timeframe selectors; query functions                                                              |       |
| Excellent    | Dashboard auto-installed (e.g., ConfigMap)                                                                                            |       |

---

## A4: ML Configuration Management & ML Testing

### Automated Tests
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | No automated tests                                                                                                                    |       |
| Poor         | Tests exist but ignore ML Test Score                                                                                                  |       |
| Sufficient   | Tests follow ML Test Score; cover all 4 categories                                                                                   |       |
| Good         | Non-determinism tests; non-functional tests; feature cost tests                                                                       |       |
| Excellent    | Terminal test adequacy reports; coverage.py; mutamorphic testing w/ auto-repair                                                      |       |

### Continuous Training
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | No automation for tests/linters                                                                                                       |       |
| Poor         | Partial automation (tests OR linters)                                                                                                 |       |
| Sufficient   | GitHub workflow runs tests + linters; `pytest`/`pylint` on push                                                                       |       |
| Good         | Test adequacy metrics (e.g., ML Test Score); coverage measured                                                                        |       |
| Excellent    | README auto-updates: test adequacy/coverage/pylint scores                                                                             |       |

### Project Organization
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | Code in notebooks/single script; no structure                                                                                         |       |
| Poor         | Partial stage separation; no layout compliance                                                                                        |       |
| Sufficient   | Python project; separated pipeline stages; dependency declaration; Cookiecutter-inspired                                              |       |
| Good         | Auto-download datasets; exploratory/prod code separation; minimal source                                                              |       |
| Excellent    | Model packaged as versioned GitHub release                                                                                            |       |

### Pipeline Management with DVC
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | No DVC pipeline                                                                                                                       |       |
| Poor         | Incomplete/failing stages                                                                                                             |       |
| Sufficient   | Runs via `dvc repro`; dependencies/outputs defined; reproducible; remote storage used                                                 |       |
| Good         | Cloud remote storage (e.g., Google Drive); setup docs; rollback support; accuracy metrics in JSON                                     |       |
| Excellent    | Metrics registered in pipeline; `dvc exp show` support; metrics beyond accuracy                                                       |       |

### Code Quality
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | No project-specific `pylint` config                                                                                                   |       |
| Poor         | Custom config but warnings/errors                                                                                                     |       |
| Sufficient   | Valid custom config; no warnings                                                                                                      |       |
| Good         | Multiple linters (e.g., flake8, Bandit)                                                                                               |       |
| Excellent    | Custom `pylint` rules for ML-specific smells                                                                                          |       |

---

## A5: Istio Service Mesh

### Traffic Management
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | No Gateway/VirtualService                                                                                                             |       |
| Poor         | Gateway/VirtualService misconfigured (inaccessible)                                                                                   |       |
| Sufficient   | Matches in-class exercise; Gateway+VirtualService; accessible via IngressGateway                                                     |       |
| Good         | DestinationRules for 90/10 routing; consistent app/model-service versions                                                             |       |
| Excellent    | Sticky sessions for stable routing                                                                                                    |       |

### Additional Use Case
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | No additional use case / inadequate complexity                                                                                        |       |
| Poor         | Attempted but non-functional                                                                                                          |       |
| Sufficient   | Partial implementation with observable effects                                                                                        |       |
| Good         | Functional but with minor flaws                                                                                                       |       |
| Excellent    | Fully functional implementation                                                                                                       |       |

### Continuous Experimentation
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | Missing deployments/metrics                                                                                                           |       |
| Poor         | Incomplete docs/implementation                                                                                                        |       |
| Sufficient   | `docs/continuous-experimentation.md` describes experiment; 2 service versions; metric for hypothesis                                  |       |
| Good         | Prometheus collects metric; Grafana dashboard; visualization screenshot                                                               |       |
| Excellent    | Detailed decision process for hypothesis acceptance/rejection                                                                         |       |

### Deployment Documentation
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | Incomprehensible/incomplete                                                                                                           |       |
| Poor         | Limited to structure OR data flow                                                                                                     |       |
| Sufficient   | Describes structure + data flow + dynamic routing; visualizations                                                                     |       |
| Good         | Covers all resources/relations; clear effects                                                                                         |       |
| Excellent    | Visually clear; enables design contributions                                                                                          |       |

### Extension Proposal
| Level        | Criteria                                                                                                                               | Grade |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------|-------|
| Insufficient | Unrelated to release engineering                                                                                                      |       |
| Poor         | Trivial/irrelevant proposal                                                                                                           |       |
| Sufficient   | Addresses release-engineering shortcoming; genuine; cites sources                                                                    |       |
| Good         | Critical reflection; measurable improvement; experiment design                                                                        |       |
| Excellent    | Generalizable solution; clearly overcomes shortcoming                                                                                 |       |