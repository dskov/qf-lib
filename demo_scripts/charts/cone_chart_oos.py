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

import matplotlib.pyplot as plt

from demo_scripts.demo_configuration.demo_ioc import container
from qf_lib.common.enums.price_field import PriceField
from qf_lib.common.tickers.tickers import QuandlTicker
from qf_lib.common.utils.dateutils.string_to_date import str_to_date
from qf_lib.data_providers.general_price_provider import GeneralPriceProvider
from qf_lib.plotting.charts.cone_chart_oos import ConeChartOOS

start_date = str_to_date('1996-01-01')
end_date = str_to_date('2012-03-01')
live_start_date = str_to_date('2012-01-01')


def main():
    data_provider = container.resolve(GeneralPriceProvider)
    tms = data_provider.get_price(QuandlTicker('AAPL', 'WIKI'), PriceField.Close, start_date, end_date)

    tms = tms.to_log_returns()
    is_tms = tms.loc[tms.index < live_start_date]
    oos_tms = tms.loc[tms.index >= live_start_date]

    is_mean_return = is_tms.mean()
    is_sigma = is_tms.std()

    cone_chart = ConeChartOOS(oos_tms, is_mean_return, is_sigma)
    cone_chart.plot()

    plt.show(block=True)


if __name__ == '__main__':
    main()
