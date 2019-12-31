import pandas as pd
from onadata.apps.fieldsight.models import Site


def time_report():
    query = Site.objects.values('id', 'date_created')
    df_site = pd.DataFrame(list(query), columns=['id', 'date_created'])
    df_site = df_site.set_index('date_created')

    weekley_df = df_site.resample('W').size().to_frame('cnt')
    weekley_df['cumsum'] = weekley_df.cnt.cumsum()
