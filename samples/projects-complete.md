# Project Topology & Principle Lattice

> Example of a completed projects.md showing populated principle lattice and project threads.

## Conceptual Threads

### Thread: Infrastructure & Automation

```
deployment-cli ──────────── monitoring-dashboard
       │                           │
       │  SSH orchestration        │  real-time metrics
       │  multi-server deploys     │  alerting rules
       │  rollback support         │  historical data
       │                           │
       └──────── shared: infrastructure as code,
                 visibility into operations,
                 reproducible environments
```

**Core idea**: Infrastructure should be transparent, automated, and auditable. No manual server tweaks, no undocumented configurations.

### Thread: Documentation & Knowledge

```
team-wiki ────────────── api-docs ────────────── runbooks
     │                       │                       │
     │  Obsidian-based       │  OpenAPI specs        │  incident response
     │  graph of knowledge   │  auto-generated       │  step-by-step guides
     │  cross-linked         │  from code            │  tested procedures
     │                       │                       │
     └──────── shared: documentation as first-class artifact,
               kept close to the code, single source of truth
```

**Core idea**: Documentation isn't afterthought - it's how knowledge survives team changes.

## Principle Lattice

> Each principle is a pattern that recurs across projects. 5-9 principles is the target; 3-8 instantiations per principle shows healthy coverage.

### Automation Over Manual

*If I do it twice, automate it.*

**Instantiations**:
- **infrastructure**: Terraform modules for common patterns; no clicking through consoles
- **deployment**: CI/CD pipelines; deploys are button presses, not procedures
- **testing**: automated test suites; manual QA is for edge cases only
- **documentation**: API docs generated from code; runbooks tested by automation
- **personal**: email filters and rules; recurring calendar blocks

### Explicit Over Implicit

*Configuration should be readable. No magic.*

**Instantiations**:
- **code**: prefer explicit parameters over convention-based defaults
- **infrastructure**: all settings in version-controlled config files
- **process**: documented decision trees over tribal knowledge
- **communication**: written agreements over verbal handshakes

### Local-First

*Don't depend on services that can disappear.*

**Instantiations**:
- **data**: SQLite for small projects; PostgreSQL self-hosted for larger
- **tools**: CLI tools that work offline; cloud features are optional enhancements
- **documentation**: markdown files in repos; wiki software is rendering layer
- **development**: dev environment runs without network

### Single Source of Truth

*One source, many views. Derived state over duplicated state.*

**Instantiations**:
- **data**: database is truth; dashboards are views
- **config**: environment files are truth; running config is derived
- **documentation**: code comments are truth for API behavior
- **status**: task frontmatter is truth; dashboards are computed

### Visibility

*What matters should be observable.*

**Instantiations**:
- **infrastructure**: logging and metrics on all services; alert on anomalies
- **code**: structured logging; trace IDs through request chains
- **process**: status tracked in shared systems; no work hidden in heads
- **incidents**: post-mortems published; learnings accessible

### Reversibility

*Prefer changes that can be undone.*

**Instantiations**:
- **deployment**: blue-green deploys; instant rollback capability
- **data**: soft deletes over hard deletes; migrations that can reverse
- **decisions**: time-boxed experiments over permanent commitments
- **architecture**: loose coupling so components can be replaced

## Project Maturity Spectrum

```
Research          Building           Mature             Complete
────────────────────────────────────────────────────────────────
new-api-design    mobile-app (60%)   deployment-cli     internal-wiki
cost-analysis     monitoring (80%)   team-wiki          onboarding-docs
                  api-docs           auth-service
```

## Tech Stack Reference

| Project | Stack | Status |
|---------|-------|--------|
| deployment-cli | Go, SSH, YAML config | Production |
| monitoring-dashboard | Grafana, Prometheus, InfluxDB | Production |
| team-wiki | Obsidian, Git, GitHub Pages | Production |
| api-docs | OpenAPI, Redoc, CI/CD | Production |
| mobile-app | React Native, TypeScript | Building (60%) |
| auth-service | Node.js, PostgreSQL, JWT | Production |

## Maintaining the Lattice

Growth protocols for healthy principle lattice:

- **Target 5-9 principles**: fewer suggests incomplete articulation, more suggests conflation
- **3-8 instantiations per principle**: fewer is just a preference, more is too broad
- **Domain coverage**: mature principles appear across multiple domains (code, infra, process, communication)
- **Compression test**: can one principle derive another? Merge them.

When to add a principle:
- You notice yourself caring about the same thing in different contexts
- A decision feels obviously right but you can't immediately say why
- You disagree with conventional wisdom and can articulate why

---

## Related

- [[voice.md]] - Thinking patterns and collaboration style
- [[../CLAUDE.md]] - System ground truth
