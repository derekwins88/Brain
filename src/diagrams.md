# System Diagram

Here’s the “capsule pipeline” at a glance:

```mermaid
flowchart LR
  A[Notes / Sketches] --> B[Capsule Draft (JSON/MD)]
  B --> C[CI Lint + Hash]
  C --> D[mdBook Render]
  D --> E[GitHub Pages]
  C --> F[Proof Tooling (future: Lean)]
```

How to update: create/edit markdown files under src/, commit, push to main.
CI rebuilds and deploys automatically.
