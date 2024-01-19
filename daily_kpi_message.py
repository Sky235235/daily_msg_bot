# -*- coding: utf-8 -*-
import daily_summary
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_figure(value):
    if value > 0:
        figure = "🔼"
    else:
        figure = "🔽"
    return figure


def get_text_value(this_df, last_df, col_name):
    this_value = list(this_df[f'{col_name}'])[0]
    last_value = list(last_df[f'{col_name}'])[0]
    diff = this_value - last_value
    diff_figure = get_figure(diff)
    t_diff = abs(diff)
    if last_value == 0:
        diff_rate = 0
    else:

        diff_rate = round((t_diff / last_value) * 100, 2)
    return this_value, last_value, t_diff, diff_rate, diff_figure

class summary_kpi:
    def __init__(self, df):
        self.df = df
    def daily_summary(self):
        df = self.df
        this_week_summary = df[df['week'] == 'this_week'].reset_index()
        last_week_summary = df[df['week'] == 'last_week'].reset_index()

        ## 매출
        _white_sales_col = '화이트_매출'
        _this_white_sales, _last_white_sales, _white_sales_diff, _white_diff_rate, _white_diff_figure = get_text_value(this_week_summary, last_week_summary, _white_sales_col)
        _black_sales_col = '하이블랙_매출'
        _this_black_sales, _last_black_sales, _black_sales_diff, _black_diff_rate, _black_diff_figure = get_text_value(this_week_summary, last_week_summary, _black_sales_col)
        ## 이용료
        _white_fee_col = '화이트_호출료'
        _this_white_fee, _last_white_fee, _white_fee_diff, _white_fee_rate, _white_fee_figure = get_text_value(this_week_summary, last_week_summary, _white_fee_col)
        _black_fee_col = '하이블랙_호출료'
        _this_black_fee, _last_black_fee, _black_fee_diff, _black_fee_rate, _black_fee_figure = get_text_value(this_week_summary, last_week_summary, _black_fee_col)
        ## 하차건수
        _white_cnt_col = '화이트_하차건수'
        _this_white_cnt, _last_white_cnt, _white_cnt_diff, _white_cnt_rate, _white_cnt_figure = get_text_value(this_week_summary, last_week_summary, _white_cnt_col)
        _black_cnt_col = '하이블랙_하차건수'
        _this_black_cnt, _last_black_cnt, _black_cnt_diff, _black_cnt_rate, _black_cnt_figure = get_text_value(this_week_summary, last_week_summary, _black_cnt_col)

        text = f'1.매출 \n' \
               f'🔸화이트 {int(_this_white_sales):,}원[{_white_diff_figure}{int(_white_sales_diff):,}원 ({_white_diff_rate}%)] \n' \
               f'🔸하이블랙 {int(_this_black_sales):,}원[{_black_diff_figure}{int(_black_sales_diff):,}원 ({_black_diff_rate}%)]\n' \
               f'\n' \
               f'2.이용료 \n' \
               f'🔸화이트 {int(_this_white_fee):,}원[{_white_fee_figure}{int(_white_fee_diff):,}원 ({_white_fee_rate}%)] \n' \
               f'🔸하이블랙 {int(_this_black_fee):,}원[{_black_fee_figure}{int(_black_fee_diff):,}원 ({_black_fee_rate}%)] \n' \
               f'\n' \
               f'3.하차건수 \n' \
               f'🔸화이트 {int(_this_white_cnt):,}건[{_white_cnt_figure}{int(_white_cnt_diff):,}건 ({_white_cnt_rate}%)] \n' \
               f'🔸하이블랙 {int(_this_black_cnt):,}건[{_black_cnt_figure}{int(_black_cnt_diff):,}건 ({_black_cnt_rate}%)] \n'

        return text

class daily_kpi:
    def __init__(self, df):
        self.df = df
        self.total_agg = daily_summary.get_daily_bot_kpi(df)

    def daily_kpi(self):
        total_agg = self.total_agg
        print(total_agg)
        ### Get Daily_BOT
        print('make send message')
        this_week_agg = total_agg[total_agg['week'] == 'this_week'].reset_index()
        last_week_agg = total_agg[total_agg['week'] == 'last_week'].reset_index()

        ### 수요
        demand_col = '수요'
        t_this_demand, t_last_demand, t_demand_diff, t_demand_diff_rate, t_demand_diff_figure = get_text_value(this_week_agg, last_week_agg, demand_col)
        ### 매출
        sale_col = '매출'
        t_this_sales, t_last_sales, t_sales_diff, t_sales_diff_rate, t_sales_diff_figure = get_text_value(this_week_agg, last_week_agg, sale_col)
        ### 호출료
        call_fee_col = '즉시호출_호출료'
        t_this_call_fee, t_last_call_fee, t_call_fee_diff, t_call_fee_rate, t_call_fee_figure = get_text_value(this_week_agg, last_week_agg, call_fee_col)
        call_fee_res_col = '예약호출_호출료'
        t_this_call_fee_res, t_last_call_fee_res, t_call_fee_diff_res, t_call_fee_rate_res, t_call_fee_figure_res = get_text_value(this_week_agg, last_week_agg, call_fee_res_col)
        ### 하차건수(즉시호출)
        pickoff_cnt = '앱호출_하차건수'
        t_this_pickoff_cnt, t_last_pickoff_cnt, t_pickoff_cnt_diff, t_pickoff_cnt_rate, t_pickoff_figure = get_text_value(this_week_agg, last_week_agg, pickoff_cnt)
        ### 배회하차건수
        general_cnt = '배회_하차수'
        t_this_general_cnt, t_last_general_cnt, t_general_cnt_diff, t_general_cnt_rate, t_general_figure = get_text_value(this_week_agg, last_week_agg, general_cnt)
        ### 예약건수
        res_cnt = '예약_하차수'
        t_this_res_cnt, t_last_res_cnt, t_res_cnt_diff, t_res_cnt_rate, t_res_figure = get_text_value(this_week_agg, last_week_agg, res_cnt)
        ### 즉시호출 배차율
        call_rate_col = '즉시호출_배차율'
        t_this_dispatch_rate, t_last_dispatch_rate, t_rate_diff, t_rate_diff_rate, t_rate_figure = get_text_value(this_week_agg, last_week_agg, call_rate_col)
        ### 즉시호출 하차율
        pickoff_rate_col = '즉시호출_하차율'
        t_this_pickoff_rate, t_last_pickoff_rate, t_pickoff_rate_diff, t_pickoff_diff_rate, t_pickoff_rate_figure = get_text_value(this_week_agg, last_week_agg, pickoff_rate_col)
        ### 즉시호출 평균 픽업시간
        call_ata_col = '즉시_평균ATA'
        t_this_ata, t_last_ata, t_ata_diff, t_ata_diff_rate, t_ata_figure = get_text_value(this_week_agg, last_week_agg, call_ata_col)

        ### 메세지 정리
        text = f'수요 {t_this_demand:,}건[{t_demand_diff_figure}{t_demand_diff:,}건({t_demand_diff_rate}%)] \n' \
               f'매출 {int(t_this_sales):,}원[{t_sales_diff_figure}{int(t_sales_diff):,}원 ({t_sales_diff_rate}%)] \n' \
               f'즉시호출 이용료 {int(t_this_call_fee):,}원[{t_call_fee_figure}{int(t_call_fee_diff):,}원({t_call_fee_rate}%)] \n' \
               f'예약호출 이용료 {int(t_this_call_fee_res):,}원[{t_call_fee_figure_res}{int(t_call_fee_diff_res):,}원({t_call_fee_rate_res}%)] \n' \
               f'앱호출 하차수 {t_this_pickoff_cnt:,}건[{t_pickoff_figure}{t_pickoff_cnt_diff:,}건 ({t_pickoff_cnt_rate}%)] \n' \
               f'배회 하차수 {t_this_general_cnt:,}건[{t_general_figure}{t_general_cnt_diff:,}건({t_general_cnt_rate}%)] \n' \
               f'예약건수 {t_this_res_cnt:,}건[{t_res_figure}{t_res_cnt_diff:,}건({t_res_cnt_rate}%)] \n' \
               f'앱호출 배차율 {t_this_dispatch_rate}%[{t_rate_figure}{t_rate_diff:.2f}%] \n' \
               f'앱호출 하차율 {t_this_pickoff_rate}%[{t_pickoff_rate_figure}{t_pickoff_rate_diff:.2f}%] \n' \
               f'앱호출 평균ATA {t_this_ata}분[{t_ata_figure}{t_ata_diff:.2f}분] \n'

        return text

    def daily_kpi_visual(self, title):
        origin_df = self.df
        df = origin_df[origin_df['week'] == 'this_week'].reset_index(drop=True)
        fill_col = ['수요', '즉시호출건수', '즉시호출_배차수', '즉시호출_하차수', '배회_하차수', '예약_하차수', '매출', '즉시호출_호출료', '예약호출_호출료']
        df[fill_col] = df[fill_col].fillna(0)
        df['앱호출수'] = df['즉시호출건수']
        df['앱호출_하차건수'] = df['즉시호출_하차수']
        df['배차율'] = round(df['즉시호출_배차수'] / df['즉시호출건수'], 2)
        df['배차율'] = df['배차율'].fillna(0)

        print('make visualization')
        kpi_fig = go.Figure()
        kpi_fig.add_trace(go.Bar(x=df['datetime_group'], y=df['앱호출_하차건수'], name='앱호출하차수', opacity=0.5))
        kpi_fig.add_trace(go.Bar(x=df['datetime_group'], y=df['배회_하차수'], name='배회하차수', opacity=0.5))
        kpi_fig.add_trace(go.Bar(x=df['datetime_group'], y=df['예약_하차수'], name='예약하차수', opacity=0.5))
        kpi_fig.add_trace(go.Scatter(x=df['datetime_group'],
                                     y=df['앱호출수'],
                                     mode='lines+markers',
                                     name='앱호출수'))
        kpi_fig.add_trace(go.Scatter(x=df['datetime_group'],
                                     y=df['this_flexible_rate'],
                                     mode='lines',
                                     name='탄력배율',
                                     yaxis='y2'))

        kpi_fig.add_trace(go.Scatter(x=df['datetime_group'],
                                     y=df['last_flexible_rate'],
                                     name='지난 주 탄력배율',
                                     yaxis='y2',
                                     line=dict(color='gray'),
                                     opacity=0.5))

        kpi_fig.add_trace(go.Scatter(x=df['datetime_group'],
                                     y=df['배차율'],
                                     line=dict(dash='dash', color='black'),
                                     name='배차율',
                                     yaxis='y2',
                                     opacity=0.5))

        kpi_fig.add_trace(go.Scatter(x=df['datetime_group'],
                                     y=[1] * len(df['datetime_group']),
                                     line=dict(dash='dot', color='black'),
                                     name='1.0기준선',
                                     yaxis='y2',
                                     opacity=0.9))

        kpi_fig.update_layout(
            xaxis=dict(domain=[0, 1]),
            yaxis=dict(title='하차수'),
            yaxis2=dict(title='탄력 배율',
                        anchor='x',
                        overlaying='y',
                        side='right'
                        )

        )
        kpi_fig.update_layout(barmode='stack', xaxis_tickangle=-45, width=1980, height=800, title=title)
        kpi_fig.update_layout(
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

        return kpi_fig

class daily_magic_kpi:
    def __init__(self, df):
        self.df = df
        self.total_agg = daily_summary.get_daily_bot_magic_kpi(df)

    def daily_magic_kpi(self):
        total_agg = self.total_agg
        print(total_agg)
        ### Get Daily_BOT
        print('make send message')
        this_week_agg = total_agg[total_agg['week'] == 'this_week'].reset_index()
        last_week_agg = total_agg[total_agg['week'] == 'last_week'].reset_index()

        ### 호출
        demand_col = '호출수'
        t_this_demand, t_last_demand, t_demand_diff, t_demand_diff_rate, t_demand_diff_figure = get_text_value(this_week_agg, last_week_agg, demand_col)
        ### 매출
        sale_col = '매출'
        t_this_sales, t_last_sales, t_sales_diff, t_sales_diff_rate, t_sales_diff_figure = get_text_value(this_week_agg, last_week_agg, sale_col)
        ### 호출료
        call_fee_col = '호출료'
        t_this_call_fee, t_last_call_fee, t_call_fee_diff, t_call_fee_rate, t_call_fee_figure = get_text_value(this_week_agg, last_week_agg, call_fee_col)
        ###
        pickoff_cnt = '하차수'
        t_this_pickoff_cnt, t_last_pickoff_cnt, t_pickoff_cnt_diff, t_pickoff_cnt_rate, t_pickoff_figure = get_text_value(this_week_agg, last_week_agg, pickoff_cnt)
        ### 배차율
        call_rate_col = '배차율'
        t_this_dispatch_rate, t_last_dispatch_rate, t_rate_diff, t_rate_diff_rate, t_rate_figure = get_text_value(this_week_agg, last_week_agg, call_rate_col)
        ### 하차율
        pickoff_rate_col = '하차율'
        t_this_pickoff_rate, t_last_pickoff_rate, t_pickoff_rate_diff, t_pickoff_diff_rate, t_pickoff_rate_figure = get_text_value(this_week_agg, last_week_agg, pickoff_rate_col)
        ### 평균 픽업시간
        call_ata_col = '매직라이드_평균ATA'
        t_this_ata, t_last_ata, t_ata_diff, t_ata_diff_rate, t_ata_figure = get_text_value(this_week_agg, last_week_agg, call_ata_col)

        ### 메세지 정리
        text = f'수요 {t_this_demand:,}건[{t_demand_diff_figure}{t_demand_diff:,}건({t_demand_diff_rate}%)] \n' \
               f'매출 {int(t_this_sales):,}원[{t_sales_diff_figure}{int(t_sales_diff):,}원 ({t_sales_diff_rate}%)] \n' \
               f'이용료 {int(t_this_call_fee):,}원[{t_call_fee_figure}{int(t_call_fee_diff):,}원({t_call_fee_rate}%)] \n' \
               f'하차수 {t_this_pickoff_cnt:,}건[{t_pickoff_figure}{t_pickoff_cnt_diff:,}건 ({t_pickoff_cnt_rate}%)] \n' \
               f'배차율 {t_this_dispatch_rate}%[{t_rate_figure}{t_rate_diff:.2f}%] \n' \
               f'하차율 {t_this_pickoff_rate}%[{t_pickoff_rate_figure}{t_pickoff_rate_diff:.2f}%] \n' \
               f'평균ATA {t_this_ata}분[{t_ata_figure}{t_ata_diff:.2f}분] \n'

        return text

    def daily_magic_kpi_visual(self, title):
        origin_df = self.df
        df = origin_df[origin_df['week'] == 'this_week'].reset_index(drop=True)
        fill_col = ['호출수', '배차수', '하차수', '매출', '호출료']
        df[fill_col] = df[fill_col].fillna(0)
        df['배차율'] = round(df['배차수'] / df['호출수'], 2)
        df['배차율'] = df['배차율'].fillna(0)
        print('make magic_visualization')
        kpi_fig = go.Figure()
        kpi_fig.add_trace(go.Bar(x=df['datetime_group'], y=df['화이트_하차수'], name='화이트_하차수', opacity=0.5))
        kpi_fig.add_trace(go.Bar(x=df['datetime_group'], y=df['하이블랙_하차수'], name='하이블랙_하차수', opacity=0.5))
        kpi_fig.add_trace(go.Scatter(x=df['datetime_group'],
                                     y=df['호출수'],
                                     mode='lines+markers',
                                     name='매직라이드_호출수'))
        kpi_fig.add_trace(go.Scatter(x=df['datetime_group'],
                                     y=df['배차율'],
                                     line=dict(dash='dash', color='black'),
                                     name='배차율',
                                     yaxis='y2',
                                     opacity=0.9))

        kpi_fig.update_layout(
            xaxis=dict(domain=[0, 1]),
            yaxis=dict(title='하차수'),
            yaxis2=dict(title='배차율',
                        anchor='x',
                        overlaying='y',
                        side='right'
                        )

        )
        kpi_fig.update_layout(barmode='stack', xaxis_tickangle=-45, width=1980, height=800, title=title)
        kpi_fig.update_layout(
            legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                )
        )

        return kpi_fig


