## 2025-05-15 - [Combined Regex for Glob Matching]
**Learning:** Replacing a loop of `fnmatch.fnmatch` calls with a single combined regex (using `fnmatch.translate` and `re.compile('|'.join(...))`) can provide a 90%+ performance boost for file filtering tasks.
**Action:** Always consider combining multiple glob/regex patterns into a single regex for high-frequency filtering logic.

## 2025-05-15 - [Avoid Redundant fnmatch Checks]
**Learning:** Found an anti-pattern where `fnmatch.fnmatch` was called multiple times for the same input and pattern due to unnecessary conditional checks (`elif '*' in pattern...`).
**Action:** Clean up redundant conditional logic in performance-critical paths.

## 2026-02-07 - [Pydantic Schema Generation Overhead]
**Learning:** Pydantic's `model_json_schema()` is significantly slower (~0.4ms) than `copy.deepcopy()` of a pre-computed schema (~0.02ms). Caching the schema generation and returning a deepcopy provides a safe 17x speedup for frequently accessed tool definitions.
**Action:** Always cache Pydantic schema generation for static models, but return a deepcopy if the result is mutable and exposed publicly.
