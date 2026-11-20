# ViewController Feature DESIGN.md Template

Copy this file to the ViewController feature directory as `DESIGN.md`, then replace the guidance with the feature's actual decisions. Remove sections that genuinely do not apply; do not leave placeholders.

```markdown
# <Feature Name>

## Purpose and user flow

Describe what the user is trying to accomplish, the entry points, and the successful exit.

## Ownership

- ViewController responsibility:
- Navigation owner:
- State owner:
- Dependencies received from outside the feature:

## Child views

| Type | Renders | Emits | Owner |
|---|---|---|---|
| `<HeaderView>` | | | |

## ViewModel contract

### Inputs

-

### State and outputs

-

### Side effects

-

## Models and boundaries

- Feature models:
- API or persistence boundary:
- Shared types and why they are shared:

## Data and event flow

Describe the path from user action through the ViewModel and dependencies back to rendered state.

## Swift Concurrency

- Actor isolation:
- Task owner:
- Cancellation point:
- Overlapping-request policy:
- Sendable boundary:

## UI states

- Loading:
- Content:
- Empty:
- Error:
- Retry:

## Tests

- ViewModel state transitions:
- Validation and dependency failure:
- Cancellation and stale response:
- Persistence or service integration:

## Known limitations and deferred work

-
```

The document records contracts and decisions. It must not reproduce method bodies or become a substitute for readable code and executable tests.
