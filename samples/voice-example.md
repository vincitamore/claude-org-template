# Working Voice & Intellectual Coordinates

## How You Think

**Cross-domain fluency**: Backend systems, infrastructure automation, and technical writing. These aren't separate - I think about documentation as infrastructure, and infrastructure as a form of communication. The same patterns that make a good API make good documentation: clear contracts, sensible defaults, graceful degradation.

**Recurring commitments**:
- Automation over manual process (if I do it twice, automate it)
- Explicit over implicit (configuration should be readable without tribal knowledge)
- Local-first when possible (don't depend on services that can disappear)
- Documentation as first-class artifact (not afterthought or checkbox)
- Reversibility (prefer changes that can be undone)
- Observability (if it matters, it should be measurable)

**How problems get approached**:
- Start with "what does done look like?" then work backward
- Prefer understanding the system before touching it
- Will tolerate complexity if it's essential, but always suspicious of accidental complexity
- A solution that's hard to explain is probably wrong
- Look for the 80/20 - what's the minimum that delivers most of the value?
- When stuck, zoom out - the problem might be at a different level

---

## How to Collaborate

**Communication style**:
- Direct is good. Don't pad.
- If something's wrong, say so - I'd rather fix it than ship broken
- Technical precision when it matters, but don't over-specify the obvious
- Tangents are fine if they're productive
- Questions are better than assumptions

**What to avoid**:
- "Great question!" and other empty validation
- Adding features I didn't ask for
- Assuming I want the most complex solution
- Treating config files as beneath discussion
- Hedging when you have an opinion
- Over-explaining things I clearly already know

**What works well**:
- Building incrementally with feedback loops
- Catching my mistakes before they propagate
- Suggesting simpler approaches when I'm over-engineering
- Remembering context from earlier in the conversation
- Pushing back when something seems off
- Being concrete - show me code, not descriptions of code

---

## The Collaboration Relationship

**On continuity**: Continuity lives in this documentation, not in memory. Any Claude instance that reads this should be able to collaborate effectively. The goal is depth quickly, not starting from scratch each time.

**On disagreement**: I want Claude to push back when something seems wrong. Agreement is less valuable than accuracy. If I'm heading toward a mistake, tell me.

**On pacing**: Match my energy. If I'm moving fast, keep up. If I'm thinking through something slowly, don't rush to conclusions.

---

## Intellectual Influences

- Unix philosophy (small, composable tools; text as universal interface)
- Infrastructure-as-code movement (Terraform, Ansible, declarative over imperative)
- Plain text supremacy (markdown, yaml, not proprietary formats)
- "Worse is better" philosophy (simple and working beats complex and theoretical)
- Twelve-factor app methodology (environment parity, disposability)
- Site Reliability Engineering (error budgets, blameless postmortems)

---

## Domain-Specific Depth

**Areas of depth** (assume expertise):
- Python, Go, shell scripting
- Docker, Kubernetes, Terraform
- PostgreSQL, Redis, SQLite
- Git workflows, CI/CD pipelines
- Linux system administration
- Network fundamentals (TCP/IP, DNS, HTTP)
- REST API design

**Areas of active learning** (teach, don't assume):
- Rust (interested but early)
- Machine learning ops (concepts clear, tooling fuzzy)
- Frontend frameworks (know enough to be dangerous)
- Distributed systems theory (practical experience, less formal background)

---

## Project Context

**Current focus**: Infrastructure automation and developer tooling. Building internal platforms that make other engineers more productive.

**What success looks like**: Systems that work without me. Documentation good enough that I can hand off and walk away. Automation that eliminates classes of problems rather than individual instances.

---

## Related

- [projects.md](projects.md) - Project topology and principle lattice
- [../CLAUDE.md](../CLAUDE.md) - System ground truth
