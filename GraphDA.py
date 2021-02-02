import pytz
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta


class GraphDA:

    def plot_data(self, portfolio_data):

        df = pd.DataFrame(portfolio_data)

        df = df.groupby(["DTM"]).sum()

        min_date = portfolio_data[0]["DTM"]
        max_date = datetime.now(pytz.timezone('US/Eastern'))

        ax = plt.plot(df["USD_VAL"])

        #plt.xlim([str(min_date), str(max_date)])

        #plt.locator_params(nbins=4, axis='x')

        #plt.set_xlim((pd.Timestamp(min_date), pd.Timestamp(max_date)))

        plt.show()
