# Use ADR to document architectural decisions

* Status: proposed
* Deciders: @rlskoeser, @thatbudakguy, @kmcelwee
* Date: 2020-12-14

Technical Story: [#37](https://github.com/Princeton-CDH/CDH_ansible/issues/37)

## Context and Problem Statement

See [#37](https://github.com/Princeton-CDH/CDH_ansible/issues/37).

## Considered Options

1. Using ADR to record decisions as single files in a folder in this repository.
2. Creating a single `CHANGELOG.md` document, as we do in application repositories.

## Decision Outcome

Option 1, since changes on this repository are not currently grouped into releases are they are in a `CHANGELOG`.

### Positive Consequences

* We can use the pull request process to propose and review architectural changes.
* Documentation for changes can use a standard template that adds detail to the decision.

### Negative Consequences

* Some extra labor is needed to fill out a template and to edit/update it once accepted.
