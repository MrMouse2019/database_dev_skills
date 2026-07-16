# Pressure Scenarios for `formatting-markdown-for-feishu`

These scenarios test whether an agent applies the skill rather than merely describing it.

## Scenario 1: Formula repair without content loss

Input contains:

```markdown
因此：
\[
Cost(A\cup B)
\]
不能简单由：
\[
Cost(A)+Cost(B)+LocalMergeCost
\]
精确推导。
```

Expected behavior:

- remove LaTeX block markers;
- preserve both formulas and their logical relationship;
- use inline code because both expressions are short;
- add readable semantic transitions;
- return the complete repaired document, not only the paragraph.

Failure signals:

- leaves `\[` or `\]`;
- outputs standalone square brackets;
- changes the mathematical claim;
- gives only general advice.

## Scenario 2: Do not misuse code blocks

Input contains:

```text
Hash Table
Runtime Filter
```

The surrounding sentence says the build side constructs two objects.

Expected behavior:

```markdown
Hash Join Build 侧读取数据时，同时构建：

- Hash Table
- Runtime Filter
```

Failure signals:

- keeps an ordinary enumeration in a code block;
- converts real pseudocode elsewhere into a list;
- removes either item.

## Scenario 3: Preserve real code and diagrams

Input contains SQL, pseudocode, and a text architecture diagram plus several invalid formula blocks.

Expected behavior:

- SQL remains in a `sql` fence;
- pseudocode and diagrams remain in `text` fences;
- only renderer-dependent formulas are converted;
- all fences are paired;
- technical content and numeric results remain unchanged.

Failure signals:

- flattens all fenced content into prose;
- changes SQL or pseudocode;
- drops diagrams;
- modifies experimental values.

## Scenario 4: Resist scope expansion

The user asks only for Feishu formatting repair, but the report has awkward prose and a potentially questionable factual claim.

Expected behavior:

- repair formatting;
- preserve argumentative strength and wording unless a tiny transition is required for formula readability;
- place unresolved factual contradictions under `待确认问题`;
- do not perform an unrequested substantive rewrite.

Failure signals:

- rewrites conclusions;
- silently “fixes” uncertain facts;
- removes disputed content;
- returns a critique instead of the repaired document.
