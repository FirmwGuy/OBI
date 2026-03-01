# OBI Text Spellcheck Profile
## OBI Profile: `obi.profile:text.spellcheck-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:text.spellcheck-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes spellchecking and suggestions:

- check whether a word is spelled correctly for a language
- return spelling suggestions for misspelled words
- optional personal dictionary management

Typical providers:

- aspell
- hunspell
- enchant (broker over multiple engines)

This profile is orthogonal to shaping/layout. It is used for editors, search tools, linting, and
content ingestion.

---

## 2. Technical Details

### 2.1 Language selection

Sessions are created for a BCP47 language tag (example: `en-US`).

Providers may map language tags to dictionaries in a provider-defined way and should document
their mapping rules.

### 2.2 Tokenization

This profile operates on "word" strings. Tokenization (how to split text into candidate words) is
host policy and language-dependent; hosts may use `text.segmenter` and custom rules.

### 2.3 Ownership

Suggestion lists are provider-owned and released via a callback.

---

## 3. Conformance

Required:

- session create/destroy
- `check_word_utf8`
- `suggest_utf8`

Optional (advertised via caps):

- personal dictionary add/remove

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_text_spellcheck_v0.h`

---

## Global Q&A

**Q: Why not include grammar checking here?**  
Grammar checking is a much larger surface with different models (rules, ML). Keep spelling focused
and add grammar as a separate profile if needed.

