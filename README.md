# pelican-summary-link

A [Pelican](https://getpelican.com/) plugin that appends a configurable link to article summaries after the `<!--more-->` marker.

## Installation

```bash
uv add pelican-summary-link
```

## Usage

Add the plugin to your Pelican configuration:

```python
PLUGINS = [
    "pelican.plugins.summary_link",
]
```

The plugin automatically appends a localized link to each article summary based on the article's `Lang` metadata.

## Settings

| Setting | Default | Description |
| --- | --- | --- |
| `SUMMARY_LINK` | *(unset)* | Override link text for all articles. Set to `""` to disable the link entirely. |
| `SUMMARY_LINK_FORMAT` | `<a class="summary-link" href="{url}">{text}</a>` | HTML template. Supports `{url}` and `{text}` placeholders. |
| `SUMMARY_LINK_TRANSLATIONS` | `{}` | Per-language link text, merged on top of built-in translations. |

### Built-in translations

| Lang | Text |
| --- | --- |
| `en` | Continue → |
| `zh-tw` | 繼續閱讀 → |
| `zh` | 繼續閱讀 → |
| `ja` | 続きを読む → |

### Resolution order

1. `SUMMARY_LINK` — explicit override, always wins (including `""` to disable)
2. `SUMMARY_LINK_TRANSLATIONS` — per-lang overrides merged on top of built-ins
3. Built-in translations matched by article `Lang`
4. `"Continue →"` fallback for unknown languages

### Examples

Disable the link globally:

```python
SUMMARY_LINK = ""
```

Add a translation for French:

```python
SUMMARY_LINK_TRANSLATIONS = {
    "fr": "Lire la suite →",
}
```

Custom link format:

```python
SUMMARY_LINK_FORMAT = '<span class="more"><a href="{url}">{text}</a></span>'
```
