---
name: swift-vc-code-review
description: Review iOS Swift changes for Swift Concurrency correctness, VC-centered feature folders, focused design documentation, useful comments, and test coverage. Use for UIKit or mixed UIKit/SwiftUI code reviews, especially when a ViewController owns child views, ViewModels, and models.
---

# Swift VC Code Review

Review the requested diff or files without modifying them unless the user separately asks for fixes.

## Review workflow

1. Establish the review range and read repository instructions before judging conventions.
2. Identify every changed ViewController and map its child views, ViewModel, models, services, and tests.
3. Read [review-rules.md](references/review-rules.md) and apply all relevant concurrency, structure, documentation, comment, and testing checks.
4. Run the smallest relevant build and test commands when the environment permits. Report commands and actual outcomes; never infer success.
5. Report only actionable findings caused or exposed by the reviewed change. Separate pre-existing issues when they materially affect safety.

## Finding format

Order findings by severity:

- **P0 Critical:** data loss, security exposure, deterministic crash, or severe concurrency corruption.
- **P1 High:** likely crash, race, actor-isolation violation, broken lifecycle, or major architecture breach.
- **P2 Medium:** incorrect behavior under realistic conditions, missing ownership boundary, missing required `DESIGN.md`, or meaningful test gap.
- **P3 Low:** maintainability issue with a concrete future cost.

Each finding must include the file and tight line range, the triggering condition, observable impact, and a specific correction. Do not report personal style preferences, generic advice, or warnings without a plausible failure mode.

If there are no actionable findings, say so explicitly and list remaining verification limits.

## Boundaries

- Treat the repository's explicit conventions as authoritative when they conflict with this skill.
- Do not demand a ViewController folder layout for pure SwiftUI features that have no ViewController.
- Do not require comments that merely narrate code. Require rationale comments only for non-obvious safety constraints described in the rules.
- A design document complements tests and readable names; it does not excuse oversized files, hidden coupling, or missing tests.
