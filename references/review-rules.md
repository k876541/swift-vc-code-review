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

## UIKit lifecycle and memory

- A task started by a ViewController must have an owner and cancellation point. Check dismissal, pop, replacement, and deinitialization paths.
- Flag task results that can update a VC after it leaves the hierarchy or overwrite newer state after a second request starts.
- Long-lived tasks stored by a VC should be cancelled during the lifecycle event that ends their usefulness; do not assume deinit happens promptly.
- Closures, Combine subscriptions, RxSwift chains, timers, notifications, delegates, and child-controller callbacks must not create a VC retain cycle.
- Table and collection view cells must cancel or identify async work during reuse so an old result cannot render into a new item.
- Repeated lifecycle entry must not create duplicate observers, subscriptions, timers, constraints, or requests.
- UI state changes must remain on the main actor even when callbacks originate from frameworks with unspecified queues.
- Loading, empty, error, and retry states must remain coherent when requests are cancelled, overlap, fail, or complete out of order.

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
- Concurrency-sensitive code needs deterministic tests; do not accept fixed sleeps, arbitrary delays, or polling as synchronization.
- Test overlapping requests so an older response cannot overwrite a newer state.
- Test cancellation during loading and confirm cancelled work does not publish success or error UI afterward.
- Test repeated taps, repeated lifecycle entry, and retry so duplicate work, observers, subscriptions, and state transitions are exposed.
- Test cell or reusable-view async work with reuse or identity changes when the feature performs asynchronous rendering.
- Repository behavior should use an in-memory persistence store or focused integration boundary when practical, including create, update, delete, ordering, and failure behavior.
- Callback and continuation bridges need tests for success, failure, cancellation, and protection against multiple completion attempts.
- Tests should exercise observable behavior with real value types and focused fakes, not assert that mocks were called without checking the resulting state.
- A `DESIGN.md` test plan is not a substitute for executable tests.

Flag missing tests only when a concrete behavior or failure mode would otherwise be unprotected. Do not request tests for trivial accessors, framework behavior, or source-code text.
