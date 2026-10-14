# Separator Chaining Table for Spider Network Parser

This table documents the separator chaining pattern for the Spider Network's robots.txt and path parsing logic. The core rule is: **spaces (tokens) are always separated by separator(s), and separators can infinitely chain as long as they continue separating spaces.**

## Grammar Rule

```
input_sequence → space (separator+ space)*
```

Where `separator+` means one or more separator characters, and these separators can be any characters (`,`, `;`, `:`, `` ` ``, etc.) that appear in a chain between two space-separated tokens.

## Examples

| Input Pattern | Separator Chain | Description |
|--------------|----------------|-------------|
| `space1:space2` | `: ` | Single separator (`:`) between two spaces |
| `space1;space2` | `; ` | Single separator (`;`) between two spaces |
| `space1,space2` | `, ` | Single separator (`,`) between two spaces |
| `space1:space2;;space3` | `:;; ` | Mixed separators chain: `:` then `;;` between space1 and space3 |
| `space1:space2;;space3,,,space4` | `:;;,,, ` | Multiple separator types chain: `:` then `;;` then `,,,` |
| `space1:space2;;space3,,,space4``pace5:::etc....` | `:;;,,,``:::etc....` | Infinite chaining of different separator types |

## Parser Behavior

The robots.txt parser (`robots_txt_parser.py`) and any path-processing modules should:

1. **Split on spaces first** — identify the tokens/spaces
2. **Between each pair of adjacent spaces, examine the separator(s)** 
3. **Accept any chain of separators** as long as they exist between the two spaces
4. **The chain ends when a new space token begins** (or at end of string)

### Parsing Logic Pseudocode

```python
def parse_separator_chain(content: str) -> list[tuple[str, str]]:
    """
    Parse a string into (space, separator_chain) tuples.
    
    Returns list of (token, separators_between_previous_and_this) pairs.
    First tuple has empty separators since there's nothing before the first token.
    """
    import re
    
    # Split into tokens and the separators between them
    # Pattern: capture spaces and the separators preceding them (except first)
    parts = re.split(r'(\s+)', content.strip())
    
    result = []
    separators = []
    
    for i, part in enumerate(parts):
        if i == 0:
            # First part: token with no preceding separators
            result.append((part, ''))
        elif part.strip() == '':
            # Empty part between separators - accumulate separators
            if separators:
                separators[-1] += part
            else:
                separators.append(part)
        else:
            # Non-empty: this is a new token
            prev_sep = separators[-1] if separators else ''
            result.append((part, prev_sep))
            separators = []  # reset for next pair
    
    return result
```

## Infinite Chain Rule

Separators **can infinitely chain** as long as they continue to separate spaces. The only stopping conditions are:

1. A new non-separator character (space token) appears
2. End of string is reached
3. An explicit non-separator, non-space character appears (depending on context)

**Example infinite chain:** `space1:::space2::::space3:::::space4` — each `:::` group separates one space from the next, and this can continue indefinitely.

## Edge Cases

| Scenario | Handling |
|----------|----------|
| `space1::space2` | Two colons `::` count as one separator chain between space1 and space2 |
| `space1 space2` | No separator → error or default behavior (context-dependent) |
| `space1::::space2` | Four colons — accepted as a single separator chain |
| `space1: :space2` | Colon-space-colon — the space breaks the chain; two separators with a space between them |

## Implementation Notes

- The existing `robots_txt_parser.py` handles `User-agent`, `Disallow`, `Allow`, and `Crawl-delay` lines with single separators
- This table extends the parser to support **chained separators** in custom/path contexts
- When integrating with the local C2 architecture (`local_c2_architecture.py`), use this pattern for access rule definitions where separators between path tokens can chain infinitely