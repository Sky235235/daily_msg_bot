from google.cloud import bigquery
from google.cloud import bigquery_storage
from google.oauth2 import service_account
import pandas as pd

def get_bigquery_data(query):

    KEY_PATH = "dataset/jinmobility-71b728241491.json"
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    bqstorage_client = bigquery_storage.BigQueryReadClient(credentials=credentials)
    query_job = client.query(query)
    df = query_job.to_dataframe(bqstorage_client=bqstorage_client)

    return df

def get_daily_bot_kpi(df):
    print('Load Daily Bot data')
    _df = df
    sum_col = ['수요',
               '즉시호출건수',
               '즉시호출_배차수',
               '즉시호출_하차수',
               '배회_하차수',
               '예약_하차수',
               '매출',
               '즉시호출_호출료',
               '예약호출_호출료'
               ]
    print('Get Daily_bot agg')
    avg_col = ['즉시_평균ATA']
    total_agg_sum = _df.groupby(['week'])[sum_col].sum().reset_index()
    total_agg_avg = _df.groupby(['week'])[avg_col].mean().reset_index()
    total_agg = pd.merge(total_agg_sum, total_agg_avg, how='left', on='week')
    total_agg['즉시호출_배차율'] = round((total_agg['즉시호출_배차수'] / total_agg['즉시호출건수']) * 100, 2)
    total_agg['즉시호출_하차율'] = round((total_agg['즉시호출_하차수'] / total_agg['즉시호출건수']) * 100, 2)
    total_agg['앱호출_하차건수'] = total_agg['즉시호출_하차수']
    total_agg['하차건수'] = total_agg['즉시호출_하차수'] + total_agg['배회_하차수']
    total_agg[avg_col] = round(total_agg[avg_col] / 60, 2)
    total_agg = total_agg.reset_index(drop=True)
    del total_agg_sum, total_agg_avg

    return total_agg

def get_daily_bot_magic_kpi(df):
    print('Load Daily Bot Magic_ride data')
    _df = df
    sum_col = ['호출수',
               '배차수',
               '화이트_배차수',
               '하이블랙_배차수',
               '하차수',
               '화이트_하차수',
               '하이블랙_하차수',
               '매출',
               '호출료'
               ]
    print('Get Daily_bot agg')
    avg_col = ['매직라이드_평균ATA', '화이트_평균ATA', '하이블랙_평균ATA']
    total_agg_sum = _df.groupby(['week'])[sum_col].sum().reset_index()
    total_agg_avg = _df.groupby(['week'])[avg_col].mean().reset_index()
    total_agg = pd.merge(total_agg_sum, total_agg_avg, how='left', on='week')
    total_agg['배차율'] = round((total_agg['배차수'] / total_agg['호출수']) * 100, 2)
    total_agg['화이트_배차율'] = round((total_agg['화이트_배차수'] / total_agg['호출수']) * 100, 2)
    total_agg['하이블랙_배차율'] = round((total_agg['하이블랙_배차수'] / total_agg['호출수']) * 100, 2)
    total_agg['하차율'] = round((total_agg['하차수'] / total_agg['호출수']) * 100, 2)
    total_agg['화이트_하차율'] = round((total_agg['화이트_배차수'] / total_agg['호출수']) * 100, 2)
    total_agg['하이블랙_하차율'] = round((total_agg['하이블랙_배차수'] / total_agg['호출수']) * 100, 2)

    total_agg[avg_col] = round(total_agg[avg_col] / 60, 2)
    total_agg = total_agg.reset_index(drop=True)
    del total_agg_sum, total_agg_avg

    return total_agg


