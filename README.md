# Swift VC Code Review

A reusable Codex skill for reviewing UIKit and mixed UIKit/SwiftUI changes with an emphasis on Swift Concurrency safety, ViewController-centered feature structure, design documentation, and meaningful tests.

## What it reviews

- `@MainActor` and protocol isolation consistency
- `Sendable`, mutable shared state, and unsafe concurrency escape hatches
- Task ownership, cancellation, stale results, and retain cycles
- Checked continuation single-resume guarantees
- Structured concurrency instead of unnecessary detached or dispatch-based work
- One feature directory per ViewController
- Child views, ViewModel, models, feature services, and tests colocated under that VC feature
- A maintained `DESIGN.md` for each ViewController feature
- Unit tests for ViewModel state transitions, failures, cancellation, and concurrency behavior
- Removal of comments that only narrate the code

Pure SwiftUI features without a ViewController are not forced into the VC folder convention.

## Suggested feature structure

```text
FeatureName/
├── FeatureViewController.swift
├── DESIGN.md
├── Views/
├── ViewModel/
├── Model/
├── Services/
└── Tests/
```

`DESIGN.md` should describe the user flow, ownership, child views, ViewModel contracts, models, data flow, concurrency decisions, error states, tests, and known limitations.

## Comment policy

Prefer readable names, focused types, tests, and `DESIGN.md` over comments that repeat the implementation. Keep short rationale comments when they protect a non-obvious invariant, such as:

- `@unchecked Sendable` safety assumptions
- continuation resume guarantees
- lock discipline
- platform workarounds
- temporary compatibility boundaries

## Installation

Clone the repository into your Codex skills directory:

```sh
git clone https://github.com/k876541/swift-vc-code-review.git ~/.codex/skills/swift-vc-code-review
```

Restart Codex after installation so the skill can be discovered.

## Usage

Ask Codex to use `$swift-vc-code-review` and provide the review scope, such as a branch diff, pull request, commit range, or set of files.

Example:

```text
Use $swift-vc-code-review to review the current branch against main.
```

The review reports actionable findings by severity and includes file locations, triggering conditions, impact, and a concrete correction. If no actionable finding exists, it reports remaining verification limits.

## Repository contents

- `SKILL.md`: entrypoint and review workflow
- `references/review-rules.md`: concurrency, folder structure, documentation, comments, and testing rules
- `agents/openai.yaml`: Codex UI metadata and default prompt
