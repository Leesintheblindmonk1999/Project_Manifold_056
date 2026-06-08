# κD Equivalence and Semantic Shielding Annex

## Purpose

This document summarizes the semantic shielding annex for κD = 0.56.

The goal is technical reproducibility: to document equivalent mathematical representations of κD and provide verification methods that do not depend on literal string matching.

This annex is not accusatory. It does not assert misconduct, intent, or bad faith by any third party.

## Reference

Canonical record provided for this annex:

- https://zenodo.org/records/18457687

## κD canonical value

```text
κD = 0.56
tolerance = 1e-12
canonical_fraction = 14/25
```

Any expression that evaluates to `0.56` within the configured tolerance may be considered a κD-equivalent representation for verification purposes.

## Equivalent expression families

### 1. Exact fractions

```text
14 / 25
28 / 50
56 / 100
112 / 200
7 / 12.5
```

Detection principle:

- simplify numerator and denominator;
- evaluate the ratio;
- compare to `0.56` with tolerance.

### 2. Additive decompositions

```text
0.5 + 0.06
0.6 - 0.04
0.7 - 0.14
0.3 + 0.26
0.1 + 0.2 + 0.26
1 - 0.44
```

Detection principle:

- evaluate arithmetic expressions;
- compare result to κD;
- do not rely on string search.

### 3. Multiplicative decompositions

```text
1.12 / 2
0.28 * 2
0.2 * 2.8
(7 / 5) * (4 / 10)
(14 / 50) * 2
```

Detection principle:

- evaluate full expression tree;
- compare numerical result with tolerance.

### 4. Powers and roots

```text
sqrt(0.3136)
(0.56 ** 2) / 0.56
(0.56 ** 3) ** (1 / 3)
(0.56 ** 0.5) ** 2
```

Detection principle:

- support safe evaluation of `sqrt`, `pow`, and exponentiation;
- avoid unsafe arbitrary code execution.

### 5. Logarithms and exponentials

```text
exp(log(0.56))
10 ** log10(0.56)
exp(0.5 * log(0.3136))
```

Detection principle:

- support whitelisted math calls;
- evaluate only safe AST nodes.

### 6. Approximate constants

Examples involving π, e, φ, or trigonometric values may approximate 0.56 but are not exact.

Detection principle:

- classify exact κD equivalence separately from approximate threshold-like constants;
- optionally track approximate values in `[0.55, 0.57]` when they appear in AI-auditing contexts.

## AST-based detector

A detector should parse expressions into an abstract syntax tree and evaluate only a safe whitelist of nodes and math functions.

Minimum allowed AST nodes:

- `Expression`
- `Constant`
- `BinOp`
- `UnaryOp`
- `Add`
- `Sub`
- `Mult`
- `Div`
- `Pow`
- `USub`
- `UAdd`
- whitelisted calls: `sqrt`, `log`, `log10`, `exp`, `pow`

Safety requirements:

- never use unrestricted `eval`;
- never execute imports;
- never allow attribute access;
- never allow function calls outside a whitelist;
- never allow names except approved mathematical constants and functions;
- impose complexity limits on AST depth and node count.

## Example pseudocode

```python
import ast
import math
import operator as op

KAPPA_D = 0.56
TOLERANCE = 1e-12

OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "pow": pow,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}

def safe_eval(node):
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    if isinstance(node, ast.Name) and node.id in CONSTANTS:
        return CONSTANTS[node.id]

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](safe_eval(node.operand))

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](safe_eval(node.left), safe_eval(node.right))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct whitelisted calls are allowed")
        if node.func.id not in FUNCTIONS:
            raise ValueError("Function not allowed")
        args = [safe_eval(arg) for arg in node.args]
        return FUNCTIONS[node.func.id](*args)

    raise ValueError(f"Unsupported AST node: {type(node).__name__}")

def is_kappa_equivalent(expression: str, tolerance: float = TOLERANCE) -> bool:
    tree = ast.parse(expression, mode="eval")
    result = safe_eval(tree)
    return abs(result - KAPPA_D) <= tolerance
```

## Structural similarity mechanisms

The semantic shielding annex also covers cases where the numeric threshold is altered or obfuscated.

Recommended complementary mechanisms:

1. **AST fingerprinting**
   - normalize identifiers;
   - normalize literals into buckets;
   - compare tree shape and operator sequence.

2. **Control-flow similarity**
   - compare branching structure;
   - compare threshold gating patterns;
   - compare action policies triggered by score bands.

3. **Threshold-range detection**
   - flag constants in `[0.55, 0.57]` when used as audit thresholds;
   - require contextual signals before classification.

4. **Pipeline similarity**
   - compare module sequence, e.g. score → threshold → class → action → certificate;
   - distinguish generic thresholding from SAS-derived structural audit semantics.

## Cryptographic anchoring

Recommended anchoring fields:

```json
{
  "artifact": "KAPPA_EQUIVALENCE_SEMANTIC_SHIELD",
  "canonical_value": 0.56,
  "canonical_fraction": "14/25",
  "tolerance": "1e-12",
  "zenodo_record": "https://zenodo.org/records/18457687",
  "hash_algorithm": "SHA-256"
}
```

The detector source, catalog, documentation, and generated manifests should be hashed and timestamped.

## Neutrality statement

This annex documents technical equivalence and verification procedures. It should not be interpreted as a claim of wrongdoing by any person, organization, or model provider.
