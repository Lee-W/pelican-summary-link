from __future__ import annotations

from pelican import contents, signals
from pelican.generators import ArticlesGenerator

DEFAULT_LINK_TEXT = "Continue \u2192"
DEFAULT_LINK_FORMAT = '<a class="summary-link" href="{url}">{text}</a>'
DEFAULT_TRANSLATIONS: dict[str, str] = {
    "en": "Continue \u2192",
    "zh-tw": "\u7e7c\u7e8c\u95b1\u8b80 \u2192",
    "zh": "\u7e7c\u7e8c\u95b1\u8b80 \u2192",
    "ja": "\u7d9a\u304d\u3092\u8aad\u3080 \u2192",
}


def _resolve_link_text(article: contents.Article) -> str:
    explicit = article.settings.get("SUMMARY_LINK")
    if explicit is not None:
        return explicit

    translations: dict[str, str] = {
        **DEFAULT_TRANSLATIONS,
        **article.settings.get("SUMMARY_LINK_TRANSLATIONS", {}),
    }
    lang: str = getattr(article, "lang", None) or article.settings.get("DEFAULT_LANG", "en")
    return translations.get(lang, DEFAULT_LINK_TEXT)


def _insert_summary_link(article: contents.Article) -> None:
    if not article._content:
        article.has_summary = False
        return

    link_text: str = _resolve_link_text(article)
    link_format: str = article.settings.get("SUMMARY_LINK_FORMAT", DEFAULT_LINK_FORMAT)

    content = article._content
    marker = content.find("<!--more-->")
    if marker == -1:
        marker = content.find("<!-- more -->")

    if marker == -1:
        if not (hasattr(article, "_summary") or "summary" in article.metadata):
            article._summary = article._content
            article.has_summary = True
        return

    summary = content[:marker]

    if link_text:
        if article.settings.get("RELATIVE_URLS"):
            url = article.url
        else:
            url = f"{article.settings.get('SITEURL', '')}/{article.url}"
        summary += link_format.format(url=url, text=link_text)

    summary = article._update_content(summary, article.get_siteurl())

    if hasattr(article, "default_status"):
        article.metadata["summary"] = summary
    else:
        article._summary = summary
    article.has_summary = True


def _run(generators: list) -> None:
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                _insert_summary_link(article)


def register() -> None:
    signals.all_generators_finalized.connect(_run)
