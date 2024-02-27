import asyncio
import os
from json import load

import pytest
from catleg.catleg import _lf_article, _skeleton
from catleg.cli_util import parse_legifrance_url
from catleg.law_text_fr import find_id_in_string
from catleg.query import (
    _article_from_legifrance_reply,
    _get_legifrance_credentials,
    get_backend,
)


def _json_from_test_file(fname):
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.dirname(path_to_current_file)
    file_path = os.path.join(current_directory, fname)
    with open(file_path, encoding="utf-8") as f:
        json_contents = load(f)
    return json_contents


@pytest.mark.skipif(
    _get_legifrance_credentials(raise_if_missing=False)[0] is None,
    reason="this test requires legifrance credentials",
)
def test_query_article():
    back = get_backend("legifrance")
    article = asyncio.run(back.article("LEGIARTI000038814944"))
    assert "logement" in article.text


@pytest.mark.skipif(
    _get_legifrance_credentials(raise_if_missing=False)[0] is None,
    reason="this test requires legifrance credentials",
)
def test_query_article_2():
    back = get_backend("legifrance")
    article = asyncio.run(back.article("CETATEXT000035260342"))
    assert article is not None


@pytest.mark.skipif(
    _get_legifrance_credentials(raise_if_missing=False)[0] is None,
    reason="this test requires legifrance credentials",
)
def test_query_article_by_url():
    article = _lf_article(
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033971416"
    )
    res = _article_from_legifrance_reply(article)
    assert "domicile" in res.text
    article_by_id = _lf_article("LEGIARTI000033971416")
    assert article["article"]["texte"] == article_by_id["article"]["texte"]


@pytest.mark.skipif(
    _get_legifrance_credentials(raise_if_missing=False)[0] is None,
    reason="this test requires legifrance credentials",
)
def test_section_skeleton():
    skel = _skeleton("LEGITEXT000031366350", "LEGISCTA000031367367")
    assert "téléservice" in skel
    skel2 = _skeleton(
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000031366350/LEGISCTA000031367367/"
    )
    assert skel == skel2


@pytest.mark.skipif(
    _get_legifrance_credentials(raise_if_missing=False)[0] is None,
    reason="this test requires legifrance credentials",
)
def test_query_articles():
    back = get_backend("legifrance")
    art1, art2 = asyncio.run(
        back.articles(["LEGIARTI000038814944", "LEGIARTI000038814948"])
    )
    assert "logement" in art1.text
    assert "pacte" in art2.text


@pytest.mark.skipif(
    _get_legifrance_credentials(raise_if_missing=False)[0] is None,
    reason="this test requires legifrance credentials",
)
@pytest.mark.parametrize("page_size", [20, 100])
def test_query_codes(page_size):
    back = get_backend("legifrance")
    codes, nb_results = asyncio.run(back._list_codes(page_size))
    assert nb_results == len(codes)


def test_no_extraneous_nota():
    article = _json_from_test_file("LEGIARTI000038814944.json")
    res = _article_from_legifrance_reply(article)
    assert "NOTA" not in res.to_markdown()
    assert "NOTA" not in res.text_and_nota()


def test_nota_format():
    article = _json_from_test_file("LEGIARTI000046790860.json")
    res = _article_from_legifrance_reply(article)
    assert "\n\nNOTA :\n\nConformément à l'article 89" in res.to_markdown()
    assert "\n\nNOTA :\n\nConformément à l'article 89" in res.text_and_nota()


def test_keep_newlines():
    article = _json_from_test_file("LEGIARTI000046790860.json")
    res = _article_from_legifrance_reply(article)
    assert "\n" in res.to_markdown()


def test_null_notas():
    article = _json_from_test_file("JORFARTI000046186676.json")
    res = _article_from_legifrance_reply(article)
    assert res.nota == ""
    assert res.nota_html == ""


def test_strip_links_from_markdown():
    article = _json_from_test_file("LEGIARTI000006302217.json")
    res = _article_from_legifrance_reply(article)
    assert "affichCodeArticle.do" not in res.to_markdown()


def test_expiry():
    article = _json_from_test_file("LEGIARTI000046790860.json")
    res = _article_from_legifrance_reply(article)
    assert res.is_open_ended

    # Conseil d'État texts do not expire
    ceta_json_article = _json_from_test_file("CETATEXT000035260342.json")
    ceta_article = _article_from_legifrance_reply(ceta_json_article)
    assert ceta_article.is_open_ended


def test_find_id_in_string():
    assert find_id_in_string("LEGIARTI000033971416", strict=True) is not None
    assert find_id_in_string("foo LEGIARTI000033971416", strict=True) is None
    assert find_id_in_string("foo LEGIARTI000033971416", strict=False) is not None


def test_parse_legifrance_urls():
    res = parse_legifrance_url(
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033971416"
    )
    assert res == ("article", "LEGIARTI000033971416")

    res = parse_legifrance_url(
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033971416/"
    )
    assert res == ("article", "LEGIARTI000033971416")

    res = parse_legifrance_url(
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069577/LEGISCTA000006197199"
    )
    assert res == ("section", "LEGITEXT000006069577", "LEGISCTA000006197199")
