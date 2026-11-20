# Swift VC Review Rules

## Swift Concurrency

- UI-owning ViewControllers, Views, ViewModels, coordinators, and observable UI state should be `@MainActor` unless a documented boundary proves otherwise.
- Protocol isolation must match conforming implementations. Flag protocols that erase an actor contract and force unsafe `nonisolated` workarounds.
- Mutable state accessed across tasks must be actor-isolated, immutable `Sendable` data, or protected by an explicit synchronization primitive.
- Values crossing actor or task boundaries must be safely `Sendable`. Treat `@unchecked Sendable` as a high-risk assertion that requires a short rationale explaining the synchronization invariant.
- Prefer structured concurrency. Flag unowned `Task` lifetimes, tasks that outlive their screen, strong captures that retain a VC, and task results applied after cancellation or navigation.
- Use `Task.detached` only for work that intentionally inherits no actor, task-local values, priority, or cancellation. Require a rationale at the call site.
- Prefer actor isolation and `MainActor.run` over `DispatchQueue.main.async` in Swift Concurrency code.
- Checked continuations must resume exactly once on every success, failure, cancellation, and early-return path.
- Cancellation must be observed before expensive work and before publishing stale UI state.
- Do not hide warnings with broad `@preconcurrency`, `nonisolated(unsafe)`, or unchecked sendability unless the boundary and risk are documented.

## VC-centered folder structure

For UIKit or mixed features owned by a ViewController, use one feature directory per VC:

```text
FeatureName/
├── FeatureViewController.swift
├── DESIGN.md
├── Views/
│   ├── FeatureHeaderView.swift
│   └── FeatureCell.swift
├── ViewModel/
│   └── FeatureViewModel.swift
├── Model/
│   └── FeatureModel.swift
├── Services/
│   └── FeatureService.swift
└── Tests/
    └── FeatureViewModelTests.swift
```

- Child views used only by that VC stay under its `Views` directory.
- The VC's ViewModel and feature-specific models stay under that VC directory.
- Feature-specific services may stay under `Services`; genuinely shared types belong in an established shared module rather than being duplicated.
- Do not move a type into a shared folder merely because another feature might use it someday.
- Flag parallel folders that split one VC's implementation across unrelated global `View`, `ViewModel`, and `Model` trees.

## Required DESIGN.md

Every VC feature directory must contain a maintained `DESIGN.md` covering:

1. Purpose and user flow.
2. Ownership and responsibility of the VC.
3. Child views and what each renders or emits.
4. ViewModel inputs, outputs, state, and side effects.
5. Models and persistence or API boundaries.
6. Data and event flow from user action to rendered state.
7. Swift Concurrency decisions: actor isolation, task ownership, cancellation, and sendability.
8. Error, loading, empty, and retry behavior.
9. Unit and integration test plan.
10. Known limitations and deferred work.

The document describes decisions and contracts, not line-by-line implementation. Flag stale documentation when it contradicts the code.

## Comments

- Reject comments that translate the next line into prose, preserve dead code, label obvious sections, or repeat type and method names.
- Prefer clear names, small functions, focused files, tests, and `DESIGN.md` for ordinary explanation.
- Keep short rationale comments for non-obvious invariants, platform bugs, temporary compatibility workarounds, continuation guarantees, lock discipline, and `@unchecked Sendable` safety arguments.
- TODO comments require an owner or issue reference when repository conventions support one, plus a concrete removal condition.

## Tests

- New ViewModel behavior needs tests for success, validation failure, dependency failure, cancellation, stale responses, and state transitions that matter to the UI.
- Concurrency-sensitive code needs deterministic tests; do not accept timing-based sleeps as synchronization.
- Tests should exercise observable behavior with real value types and focused fakes, not assert that mocks were called without checking the resulting state.
- A `DESIGN.md` test plan is not a substitute for executable tests.
