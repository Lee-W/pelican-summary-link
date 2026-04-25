from __future__ import annotations

from unittest.mock import MagicMock

from pelican.plugins.summary_link.summary_link import _insert_summary_link


def make_article(
    content: str,
    settings: dict | None = None,
    lang: str = "en",
) -> MagicMock:
    article = MagicMock()
    article._content = content
    article.has_summary = False
    article.metadata = {}
    article.url = "posts/test-article"
    article.lang = lang
    article.get_siteurl.return_value = "http://localhost:8000"
    article._update_content.side_effect = lambda s, _: s
    article.settings = {
        "SITEURL": "http://localhost:8000",
        "RELATIVE_URLS": False,
        "DEFAULT_LANG": "en",
        **(settings or {}),
    }
    del article.default_status
    return article


def test_no_more_marker_sets_full_content_as_summary():
    article = make_article("<p>Full content.</p>")
    del article._summary
    _insert_summary_link(article)
    assert article._summary == "<p>Full content.</p>"
    assert article.has_summary is True


def test_more_marker_splits_summary():
    article = make_article("<p>Intro.</p><!--more--><p>Rest.</p>")
    _insert_summary_link(article)
    assert article._summary == "<p>Intro.</p>"
    assert article.has_summary is True


def test_more_marker_with_spaces():
    article = make_article("<p>Intro.</p><!-- more --><p>Rest.</p>")
    _insert_summary_link(article)
    assert article._summary == "<p>Intro.</p>"


def test_summary_link_appended_when_text_set():
    article = make_article(
        "<p>Intro.</p><!--more--><p>Rest.</p>",
        {"SUMMARY_LINK": "Continue →"},
    )
    _insert_summary_link(article)
    assert "Continue →" in article._summary
    assert article.url in article._summary


def test_empty_link_text_skips_link():
    article = make_article(
        "<p>Intro.</p><!--more--><p>Rest.</p>",
        {"SUMMARY_LINK": ""},
    )
    _insert_summary_link(article)
    assert article._summary == "<p>Intro.</p>"


def test_empty_content_sets_has_summary_false():
    article = make_article("")
    _insert_summary_link(article)
    assert article.has_summary is False


def test_custom_link_format():
    article = make_article(
        "<p>Intro.</p><!--more-->",
        {
            "SUMMARY_LINK": "Read more",
            "SUMMARY_LINK_FORMAT": '<a href="{url}" class="custom">{text}</a>',
        },
    )
    _insert_summary_link(article)
    assert "<a href=" in article._summary
    assert 'class="custom"' in article._summary
    assert "Read more" in article._summary


def test_i18n_uses_builtin_translation_for_lang():
    article = make_article("<p>Intro.</p><!--more-->", lang="zh-tw")
    _insert_summary_link(article)
    assert "繼續閱讀 →" in article._summary


def test_i18n_falls_back_to_default_for_unknown_lang():
    article = make_article("<p>Intro.</p><!--more-->", lang="fr")
    _insert_summary_link(article)
    assert "Continue →" in article._summary


def test_i18n_custom_translation_overrides_builtin():
    article = make_article(
        "<p>Intro.</p><!--more-->",
        settings={"SUMMARY_LINK_TRANSLATIONS": {"en": "Keep reading →"}},
        lang="en",
    )
    _insert_summary_link(article)
    assert "Keep reading →" in article._summary


def test_i18n_summary_link_overrides_translations():
    article = make_article(
        "<p>Intro.</p><!--more-->",
        settings={"SUMMARY_LINK": "Override →"},
        lang="zh-tw",
    )
    _insert_summary_link(article)
    assert "Override →" in article._summary
    assert "繼續閱讀" not in article._summary
