# -*- coding: utf-8 -*-

import json
import telegram
import asyncio
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from daily_kpi_message import daily_kpi, daily_magic_kpi, summary_kpi
import daily_summary
from module.QueryConfig import GetBigQuery
from datetime import timedelta, datetime
import time
import os
import pandas as pd
import traceback

## Query Configuration
#### make date

today_date = datetime.now().date()

start_date = today_date - timedelta(days=1)
last_start_date = start_date - timedelta(days=7)
last_end_date = today_date - timedelta(days=7)

print('start_date', start_date)
print('today_date', today_date)
print('last_start_date', last_start_date)
print('last_end_date', last_end_date)

### get daily KPI data
config_query = GetBigQuery()

### 개요 데이터 로드
_summary_query = config_query.get_summary_query(start_date, today_date, last_start_date, last_end_date)
summary_df = daily_summary.get_bigquery_data(_summary_query)

## 화이트 데이터 로드
_query = config_query.get_kpi_query(start_date, today_date, last_start_date, last_end_date, 1)
base_df = daily_summary.get_bigquery_data(_query)
### 탄력배율 로드
rate_query = config_query.get_flexible_rate_query(start_date, today_date, last_start_date, last_end_date)
rate_df = daily_summary.get_bigquery_data(rate_query)
white_rate = rate_df[rate_df['car_type_idx'] == 1].reset_index(drop=True)
black_rate = rate_df[rate_df['car_type_idx'] == 3].reset_index(drop=True)
## 화이트 탄력배율 결합
white_kpi_df = pd.merge(white_rate, base_df, how='outer', on='datetime_group')

#### 하이블랙 데이터 로드
_black_query = config_query.get_kpi_query(start_date, today_date, last_start_date, last_end_date, 3)
black_base_df = daily_summary.get_bigquery_data(_black_query)
## 하이블랙 탄력배율 결합
black_kpi_df = pd.merge(black_rate, black_base_df, how='outer', on='datetime_group')

#### 매직라이드 데이터 로드
_magic_query = config_query.get_magic_kpi_query(start_date, today_date, last_start_date, last_end_date)
magic_df = daily_summary.get_bigquery_data(_magic_query)


## Message Configuration
### summary_message
summary_kpi = summary_kpi(summary_df)
summary_text = summary_kpi.daily_summary()
summary_text_message = f'{start_date}의 일간 지표 알람 입니다.\n' \
                       '[개요]\n' + summary_text

#### white message
white_daily_kpi = daily_kpi(white_kpi_df)
white_text = white_daily_kpi.daily_kpi()
white_text_message = f'\n [White 전주 같은 요일 대비 지표]\n' \
                 + '\n' + white_text

white_title = '화이트 일일 지표'
white_visual = white_daily_kpi.daily_kpi_visual(white_title)
white_image_path = f'dataset/white_daily_kpi_visual_{start_date}.png'
white_visual.write_image(white_image_path)

##### black_message
black_daily_kpi = daily_kpi(black_kpi_df)
black_text = black_daily_kpi.daily_kpi()
black_text_message = f'\n' + '\n [HiBlack 전주 같은 요일 대비 지표]\n' \
                 + '\n' + black_text

black_title = '하이블랙 일일 지표'
black_visual = black_daily_kpi.daily_kpi_visual(black_title)
black_image_path = f'dataset/black_daily_kpi_visual_{start_date}.png'
black_visual.write_image(black_image_path)

#### magic_ride_message
magic_daily_kpi = daily_magic_kpi(magic_df)
magic_text = magic_daily_kpi.daily_magic_kpi()
magic_text_message = f'\n' + '\n [매직라이드 전주 같은 요일 대비 지표]\n' \
                 + '\n' + magic_text

magic_title = '매직라이드 일일지표'
magic_visual = magic_daily_kpi.daily_magic_kpi_visual(magic_title)
magic_image_path = f'dataset/magic_daily_kpi_visual_{start_date}.png'
magic_visual.write_image(magic_image_path)

## 텔레그램 Configuration
with open('dataset/bot_config.json', 'r') as f:
    bot_config = json.load(f)
bot_token = bot_config['telegram_token']['monitoring_bot']
bot = telegram.Bot(token=bot_token)
chat_id = bot_config['telegram_chat_id'] ## 배포용
# chat_id = bot_config['telegram_test_id'] ## 테스트용

async def send_telegram_message(chat_id, text, img_path):
    await bot.send_message(chat_id, text)
    with open(img_path, 'rb') as img_file:
        await bot.send_photo(chat_id, photo=img_file)
    # with open(visual_path, 'rb') as visual_file:
    #     await bot.send_document(chat_id, document=visual_file)

async def send_messages():
    for k, v in chat_id.items():
        print(f'{k}에게 발송 중')
        await bot.send_message(v, summary_text_message)
        await send_telegram_message(v, white_text_message, white_image_path)
        await send_telegram_message(v, black_text_message, black_image_path)
        await send_telegram_message(v, magic_text_message, magic_image_path)

try:
    print('send_telegram message')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_messages())
except Exception as e:
    error_message = f'{traceback.format_exc()}'
    print(error_message)

print('Send Slack')
slack_token = bot_config['slack_token']['IM_daily_bot_token']
slack_client = WebClient(token=slack_token)
slack_channel = bot_config['slack_token']['ELAB_ID']

try:
    summary_text_message = slack_client.chat_postMessage(channel=slack_channel, text=summary_text_message)
    time.sleep(1)
    white_text_response = slack_client.chat_postMessage(channel=slack_channel, text=white_text_message)
    white_img_response = slack_client.files_upload_v2(channel=slack_channel, file=white_image_path)
    time.sleep(3)
    black_text_response = slack_client.chat_postMessage(channel=slack_channel, text=black_text_message)
    black_img_response = slack_client.files_upload_v2(channel=slack_channel, file=black_image_path)
    time.sleep(3)
    magic_text_response = slack_client.chat_postMessage(channel=slack_channel, text=magic_text_message)
    magic_img_response = slack_client.files_upload_v2(channel=slack_channel, file=magic_image_path)

except SlackApiError as e:
    print(f"Error uploading image: {e.response['error']}")

print('remove html and image')
os.remove(white_image_path)
os.remove(black_image_path)
os.remove(magic_image_path)