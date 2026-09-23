# Bug Diary
## Bug 1 — Incorrect order routing from substring matching
### Failure
A TrailPlus return query containing the word "ordered" was incorrectly routed as an order-related request because the router used substring matching for the term "order".

### Impact
The agent asked for an order ID instead of answering the TrailPlus return-policy question.

### Fix
Changed order-related keyword matching to use whole-word regular expressions so "order" matches independently without matching words such as "ordered".

### Regression
Added/updated routing tests and verified the full evaluation suite.

## Bug 2 — Incorrect evidence selection for TrailPlus returns
### Failure
A TrailPlus return question could retrieve the generic standard returns policy instead of the TrailPlus policy.

### Impact
The agent could provide the incorrect 30-day return window instead of the TrailPlus 45-calendar-day window.

### Fix
Updated evidence selection to prefer the TrailPlus membership document when the query explicitly mentions TrailPlus or the session membership tier is TrailPlus.

### Regression
Verified the TrailPlus evaluation case and full test suite.

## Bug 3 — Unfriendly order ETA date formatting
### Failure
Order lookup responses exposed ISO-formatted dates such as `2026-08-22`.

### Impact
The response was technically correct but not natural for a customer-facing answer.

### Fix
Converted ISO dates into human-readable dates such as `August 22, 2026`.

### Regression
Verified the shipped-order evaluation case.

## Bug 4 — Final-sale damaged-item exception
### Failure
Final-sale restrictions and damaged-item exceptions require information from two separate policy documents.

### Impact
A simple retrieval result could fail to combine the relevant policies.

### Fix
Added targeted evidence selection for final-sale damaged/wrong-item questions and explicitly surfaced both relevant official sources.

### Regression
Verified the final-sale damaged-item evaluation case.

## Bug 5 — Conflicting official product information
### Failure
Two official knowledge-base documents contained conflicting dishwasher-safety instructions for the Breeze Tumbler.

### Impact
The agent should not silently choose one source when authoritative sources disagree.

### Fix
Added conflict detection that identifies both sources, informs the user of the conflict, recommends the safer interim handling instruction, and hands the case to support.

### Regression
Verified the genuine active source-conflict evaluation case.