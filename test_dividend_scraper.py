import pytest

from dividend_scraper import check_company, dividend_keywords, interim_dividend_keywords, buyback_keywords


class TestDividendScraper:

    @pytest.mark.parametrize(
        "url, expect_dividend_keywords, expect_interim_dividend_keywords, expect_buyback_keywords",
        [
            (
                'https://www.investegate.co.uk/worldwide-healthcare--wwh-/prn/issue-of-equity/20200803182605PA4E1/', False, False, False
            ),
            (
                'https://www.investegate.co.uk/rotork-plc--ror-/rns/2020-half-year-results/202008040700039981U/', True, True, True
            ),
            (
                'https://www.investegate.co.uk/babcock-intnl-group--bab-/rns/result-of-agm/202008041133480914V/', False, False, True
            ),
            (
                'https://www.investegate.co.uk/caledonia-inv-plc--cldn-/rns/director-pdmr-shareholding/202008051357482589V/', False, False, False
            )
        ]
    )
    def test_check_company(self, url, expect_dividend_keywords, expect_interim_dividend_keywords, expect_buyback_keywords):
        result = check_company(url,
                      dividend_keywords=dividend_keywords,
                      interim_dividend_keywords=interim_dividend_keywords,
                      buyback_keywords=buyback_keywords
        )

        assert result['contains_dividend_keywords'] == expect_dividend_keywords, "Dividends did not match"
        assert result['contains_interim_dividend_keywords'] == expect_interim_dividend_keywords, "Interim dividends did not match"
        assert result['contains_buyback_keywords'] == expect_buyback_keywords, "Buy back did not match"