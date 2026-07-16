# Maintenance Workflows

## Ingest

1. Register URL/path, author or publisher, retrieval date, source type, applicable version, and reliability.
2. Identify affected existing pages before creating a page.
3. Update concepts and flows; record contradictions and version differences.
4. Update cross-links, index, overview when needed, and append the log.
5. Run the audit and report changes requiring human review.

Do not create one isolated summary per source when the knowledge belongs in an existing concept.

## Query

1. Read the index and select a small relevant page set.
2. Re-check drift-prone or correctness-sensitive claims against current source.
3. Distinguish facts, assumptions, hypotheses, and recommendations.
4. Cite Wiki pages and source anchors.
5. Persist only reviewed, stable conclusions.

## Migration

- Start additively; preserve existing user docs and inbound links.
- Map old pages to new domains and flows.
- Split coarse pages during source verification rather than copying them.
- Replace an old page with a migration notice only after coverage and inbound-link checks pass.
- Never delete duplicates or orphans automatically.

## Audit contract

The candidate set must be selected by path before parsing metadata. Otherwise a page with missing frontmatter becomes invisible to the audit.

Check:

- missing frontmatter and required fields;
- empty values and vocabulary;
- source paths;
- Markdown links and fragments;
- orphans and root reachability;
- duplicate titles;
- lifecycle/evidence consistency;
- terminology/redaction;
- index status drift and overview routes.

Run a negative test: create a temporary candidate page with missing frontmatter, require audit failure, remove it, then require audit success. Never report static audit success as runtime database validation.

## Review gates

For each delivery:

1. Specification review: files, scope, links, states, and acceptance criteria.
2. Technical review: source accuracy, transaction/failure semantics, evidence mapping, and unsupported claims.
3. Final branch review: coverage, consistency, maintainability, legacy preservation, and reproducibility.

Fix Critical and Important findings, regenerate evidence, and re-review.
