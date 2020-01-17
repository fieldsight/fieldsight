import datetime

import pandas as pd
from onadata.apps.fieldsight.models import Site


def time_report():
    query = Site.objects.values('id', 'date_created')
    df_site = pd.DataFrame(list(query), columns=['id', 'date_created'])
    start_date = "01-06-2016"
    end_date = datetime.date.today().strftime("%d-%m-%y%y")
    idx = pd.date_range(start_date, end_date)
    df_daily = df_site.groupby(pd.Grouper(key='date_created', freq='1D')).size().to_frame("count").reset_index()
    df_daily['date_only'] = df_daily.date.dt.date
    df_daily = df_daily.reindex('date_only')
    df_daily.reindex(idx, fill_value=0)

