#     Copyright 2016-present CERN – European Organization for Nuclear Research
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#

from datetime import datetime
from unittest import TestCase

import numpy as np
import pandas as pd
from mockito import mock, when, ANY
from numpy.testing import assert_equal, assert_almost_equal

from qf_lib.backtesting.alpha_model.alpha_model import AlphaModel
from qf_lib.backtesting.alpha_model.exposure_enum import Exposure
from qf_lib.backtesting.alpha_model.alpha_model_strategy import AlphaModelStrategy
from qf_lib.common.enums.frequency import Frequency
from qf_lib.common.enums.price_field import PriceField
from qf_lib.common.tickers.tickers import Ticker, BloombergTicker
from qf_lib.common.utils.dateutils.string_to_date import str_to_date
from qf_lib.containers.qf_data_array import QFDataArray
from qf_lib.data_providers.preset_data_provider import PresetDataProvider
from qf_lib.data_providers.data_provider import DataProvider
from qf_lib_tests.integration_tests.backtesting.trading_session_for_tests import TestingTradingSession


class TestAlphaModelStrategy(TestCase):
    tickers = [BloombergTicker("AAPL US Equity")]

    data_start_date = str_to_date("2014-12-25")
    test_start_date = str_to_date("2015-01-01")
    end_date = str_to_date("2015-02-28")
    frequency = Frequency.DAILY

    def setUp(self):
        all_fields = PriceField.ohlcv()

        self._mocked_prices_arr = self._make_mock_data_array(self.tickers, all_fields)
        self._price_provider_mock = PresetDataProvider(self._mocked_prices_arr, self.data_start_date, self.end_date,
                                                       self.frequency)

        risk_estimation_factor = 0.05
        self.alpha_model = DummyAlphaModel(risk_estimation_factor)

        self.ts = self._test_trading_session_init()
        model_tickers_dict = {self.alpha_model: self.tickers}
        AlphaModelStrategy(self.ts, model_tickers_dict, use_stop_losses=True)
        self.ts.start_trading()

    @classmethod
    def _make_mock_data_array(cls, tickers, fields):
        all_dates_index = pd.bdate_range(start=cls.data_start_date, end=cls.end_date)

        num_of_dates = len(all_dates_index)
        num_of_tickers = len(tickers)
        num_of_fields = len(fields)

        start_value = 100.0
        values = np.arange(start_value, num_of_dates * num_of_tickers * num_of_fields + start_value)
        reshaped_values = np.reshape(values, (num_of_dates, num_of_tickers, num_of_fields))

        mocked_result = QFDataArray.create(all_dates_index, tickers, fields, data=reshaped_values)
        mocked_result.loc[:, :, PriceField.Low] -= 5.0
        mocked_result.loc[:, :, PriceField.High] += 5.0
        cls._add_test_cases(mocked_result, tickers)
        return mocked_result

    @classmethod
    def _add_test_cases(cls, mocked_result, tickers):
        # single low price breaking the stop level
        mocked_result.loc[str_to_date('2015-02-05'), tickers[0], PriceField.Low] -= 15.0
        # two consecutive low prices breaking the stop level
        mocked_result.loc[str_to_date('2015-02-12'), tickers[0], PriceField.Low] -= 15.0
        mocked_result.loc[str_to_date('2015-02-13'), tickers[0], PriceField.Low] -= 15.0
        # single open price breaking the stop level
        mocked_result.loc[str_to_date('2015-02-23'), tickers[0], PriceField.Low] -= 25.0
        mocked_result.loc[str_to_date('2015-02-23'), tickers[0], PriceField.Open] = \
            mocked_result.loc[str_to_date('2015-02-23'), tickers[0], PriceField.Low]

    @classmethod
    def _create_price_provider_mock(cls, tickers, fields, result) -> DataProvider:
        price_provider_mock = mock(strict=True)
        when(price_provider_mock).get_price(tickers, fields, ANY(datetime), ANY(datetime)).thenReturn(result)

        return price_provider_mock

    def _test_trading_session_init(self):
        ts = TestingTradingSession(
            data_provider=self._price_provider_mock,
            start_date=self.test_start_date,
            end_date=self.end_date,
            initial_cash=1000000,
            frequency=self.frequency
        )
        return ts

    def test_stop_losses(self):
        result = self.ts.portfolio

        expected_transactions_quantities = \
            [8130, -127, 1, -8004, 7454, -58, -7396, 6900, -6900, 6390, -44, -6346, 5718, -36]
        result_transactions_quantities = [t.quantity for t in result.transactions_series()]
        assert_equal(expected_transactions_quantities, result_transactions_quantities)

        expected_transactions_prices = [125, 130, 135, 235.6, 255, 260, 259.35, 280, 264.1, 285, 290, 282, 315, 320]
        result_transactions_prices = [t.price for t in result.transactions_series()]
        assert_almost_equal(expected_transactions_prices, result_transactions_prices)

        expected_portfolio_values = [1024390, 1064659, 1064659, 1064659, 1104677, 1144697, 1184717, 1224737, 1264757,
                                     1264757, 1264757, 1304777, 1344797, 1384817, 1424837, 1464857, 1464857, 1464857,
                                     1504877, 1544897, 1584917, 1624937, 1664957, 1664957, 1664957, 1704977, 1744997,
                                     1785017, 1825037, 1865057, 1865057, 1865057, 1905077, 1945097, 1985117, 1885867.4,
                                     1908229.4, 1908229.4, 1908229.4, 1945325.4, 1982305.4, 2019285.4, 1918330, 1808620,
                                     1808620, 1808620, 1827790, 1859608, 1891338, 1923068, 1954798, 1954798, 1954798,
                                     1789802, 1806956, 1835438, 1863848, 1892258, 1892258]
        assert_almost_equal(expected_portfolio_values, list(result.portfolio_eod_series()))


class DummyAlphaModel(AlphaModel):
    def __init__(self, risk_estimation_factor: float):
        super().__init__(0.0, None)
        self.risk_estimation_factor = risk_estimation_factor

    def calculate_exposure(self, ticker: Ticker, current_exposure: Exposure) -> Exposure:
        return Exposure.LONG

    def calculate_fraction_at_risk(self, ticker: Ticker):
        return self.risk_estimation_factor
