# Standardize on use of "staging" for non-production application environment

* Status: accepted
* Deciders: @rlskoeser, @kayiwa, @acozine
* Date: 2024-02-23

## Context and Problem Statement

CDH applications and playbooks have been inconsistent in terminology referring to our non-production deploy environment, variously referring to it as "test", "QA", or "staging".

PUL uses "staging" to refer to their equivalent environment, and CDH applications in testing or pre-production deploy environments make use of PUL staging resources including Postgresql and Solr servers.

This name change is related to work in [PR #188](https://github.com/Princeton-CDH/cdh-ansible/pull/188), which consolidates existing playbooks to a single playbook per application with a variable to distinguish between staging and production runtime environments.  This change aligns CDH and PUL naming conventions and will hopefully avoid confusion in future.

## Considered Options

1. Continue using existing "qa" environment for CDH applications and "staging" for PUL
2. Rename CDH environment to "staging" for consistency with PUL

## Decision Outcome

Option 2, for consistency and to avoid confusion between different terms that mean the same thing.

### Positive Consequences

* Staging terminology will be consistent between CDH and PUL
* The new `runtime_env` configuration used in the consolidated playbooks can be used in playbooks and roles that formerly relied on the presence or absence of a `qa` variable

### Negative Consequences

* This change requires cleanup in playbooks, host groups, group variables
* Some legacy items may still reference qa/test nomenclature, including:
    * webpack qa build (based on application-specific configuration)
    * hostname patterns (eg. test-prosody.cdh.princeton.edu)
