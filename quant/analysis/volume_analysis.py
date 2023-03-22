#!/usr/bin/python
import copy

import pandas as pd
import numpy as np
from typing import Text, Union
import qlib
from qlib.backtest import executor, backtest
from qlib.backtest.decision import TradeDecisionWO, OrderDir, Order
from qlib.backtest.position import Position
from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.contrib.strategy.signal_strategy import BaseSignalStrategy
from qlib.data.dataset import DatasetH
from qlib.data.dataset.loader import QlibDataLoader
from qlib.data.dataset.handler import DataHandlerLP
from qlib.config import REG_CN
import matplotlib.pyplot as plt
from qlib.strategy.base import BaseStrategy
from qlib.utils import init_instance_by_config
from qlib.utils.time import Freq
from qlib.workflow import R
from qlib.workflow.record_temp import PortAnaRecord, SignalRecord
import qlib.contrib.report as qcr
from qlib.contrib.report import analysis_model, analysis_position
from model.base_model import BaseModel

import sys
import os

class VolumeFeature(DataHandlerLP):
    def __init__(self,
                 instruments='sh000300',
                 start_time=None,
                 end_time=None,
                 freq='day',
                 infer_processors=[],
                 learn_processors=[],
                 fit_start_time=None,
                 fit_end_time=None,
                 process_type=DataHandlerLP.PTYPE_A,
                 filter_pipe=None,
                 inst_processor=None,
                 **kwargs,
                 ):
        data_loader = {
            'class': 'QlibDataLoader',
            'kwargs': {
                'config': {
                    'feature': self.get_feature_config(),
                    'label': kwargs.get('label', self.get_label_config()),  # label可以自定义，也可以使用初始化时候的设置
                },
                'filter_pipe': filter_pipe,
                'freq': freq,
                'inst_processor': inst_processor,
            },
        }
        super().__init__(
            instruments=instruments,
            start_time=start_time,
            end_time=end_time,
            data_loader=data_loader,
            infer_processors=infer_processors,
            learn_processors=learn_processors,
            process_type=process_type,
        )

    def get_feature_config(self):
        VOLUME_MEAN = 'Mean($volume, 30)'

        return ['$volume', '$close', VOLUME_MEAN], ['VOLUME',  'CLOSE', 'VOLUME_MEAN']

    def get_label_config(self):
        return ['(Ref($close, -30) - $close) / $close'], ['LABEL']

class VolumeModel(BaseModel):
    def predict(self, dataset: DatasetH, segment: Union[Text, slice] = "test"):
        #dl_test = dataset.prepare(segment, col_set=["CHANGE", "CHANGE_MEAN"], data_key=DataHandlerLP.DK_I)
        dl_test = dataset.prepare(segment, col_set="__all", data_key=DataHandlerLP.DK_I)
        print("dl_test")
        print(dl_test)
        preds = dl_test["VOLUME"] - dl_test["VOLUME_MEAN"]
        print(preds)
        #print(preds.to_numpy())
        #print(pd.Series(preds.to_numpy()))
        return preds

class VolumeStrategy(BaseSignalStrategy):
    def __init__(self, **kwargs):
        print("ChangeStrategy __init__")
        print(kwargs)
        #super(ChangeStrategy, self).__init__(**kwargs)
        super().__init__(**kwargs)

    def generate_trade_decision(self, execute_result=None):
        trade_step = self.trade_calendar.get_trade_step()
        trade_start_time, trade_end_time = self.trade_calendar.get_step_time(trade_step)
        pred_start_time, pred_end_time = self.trade_calendar.get_step_time(trade_step, shift=1)
        pred_score = self.signal.get_signal(start_time=pred_start_time, end_time=pred_end_time)
        print("===============================")
        print("trade_step:", trade_step)
        print("trade_calendar:", self.trade_calendar)
        print("trade_position:", self.trade_position)
        print("pred_score:", pred_score)
        if pred_score is None:
            return TradeDecisionWO([], self)
        code = pred_score.keys()[0]
        pred = pred_score.item()

        current_temp: Position = copy.deepcopy(self.trade_position)
        cash = current_temp.get_cash()
        current_stock_list = current_temp.get_stock_list()
        print("current_stock_list: ", current_stock_list)

        # generate order list for this adjust date
        sell_order_list = []
        buy_order_list = []

        if pred > 0:
            if len(current_stock_list) > 0:
                sell_amount = current_temp.get_stock_amount(code=code)
                sell_order = Order(
                    stock_id=code,
                    amount=sell_amount,
                    start_time=trade_start_time,
                    end_time=trade_end_time,
                    direction=Order.SELL,  # 0 for sell, 1 for buy
                )
                # is order executable
                if self.trade_exchange.check_order(sell_order):
                    sell_order_list.append(sell_order)
                    trade_val, trade_cost, trade_price = self.trade_exchange.deal_order(
                        sell_order, position=current_temp
                    )
                    # update cash
                    cash += trade_val - trade_cost

        if pred < 0:
            # check is stock suspended
            if self.trade_exchange.is_stock_tradable(
                stock_id=code,
                start_time=trade_start_time,
                end_time=trade_end_time,
                direction=OrderDir.BUY,
            ):
                buy_price = self.trade_exchange.get_deal_price(
                    stock_id=code, start_time=trade_start_time, end_time=trade_end_time, direction=OrderDir.BUY
                )
                print("buy_price: ", buy_price)
                buy_amount = cash / buy_price
                factor = self.trade_exchange.get_factor(stock_id=code, start_time=trade_start_time,
                                                        end_time=trade_end_time)
                buy_amount = self.trade_exchange.round_amount_by_trade_unit(buy_amount, factor)
                buy_order = Order(
                    stock_id=code,
                    amount=buy_amount,
                    start_time=trade_start_time,
                    end_time=trade_end_time,
                    direction=Order.BUY,  # 1 for buy
                )
                buy_order_list.append(buy_order)

        print(sell_order_list + buy_order_list)
        return TradeDecisionWO(sell_order_list + buy_order_list, self)

def analysis():
    #data_handler_config = {
    #    "start_time": "2015-01-01",
    #    "end_time": "2020-03-31",
    #    "fit_start_time": "2015-01-01",
    #    "fit_end_time": "2019-03-31",
    #    "instruments": "SH600006",
    #}
    #dataset_config = {
    #    #"class": "ChangeFeature",
    #    #"module_path": "qlib.data.dataset",
    #    "kwargs": {
    #        "handler": {
    #            "class": "Alpha158",
    #            "module_path": "qlib.contrib.data.handler",
    #            "kwargs": data_handler_config,
    #        },
    #        "segments": {
    #            "train": ("2015-01-01", "2015-03-31"),
    #            "valid": ("2019-01-01", "2019-03-31"),
    #            "test": ("2020-01-01", "2020-03-31"),
    #        },
    #    },
    #}
    #dataset = init_instance_by_config(dataset_config)

    feature = VolumeFeature(instruments=['SH601288'], start_time='20180101', end_time='20200331',
                            fit_start_time="20150101", fit_end_time="20190331")
    ds = DatasetH(handler=feature,
                  step_len=40,
                  segments={
                            "train": ("2015-01-01", "2015-03-31"),
                            "valid": ("2019-01-01", "2019-03-31"),
                            "test": ("2020-01-01", "2020-03-31")})
    model = VolumeModel()
    # 需要加入自定义路径
    # export PYTHONPATH="/Users/zhangyunsheng/Dev/sonata/quant"
    port_analysis_config = {
        "strategy": {
            "class": "VolumeStrategy",
            "module_path": "volume_analysis",
            #"module_path": "analysis.change_analysis",
            #"class": "TopkDropoutStrategy",
            #"module_path": "qlib.contrib.strategy.signal_strategy",
            "kwargs": {
                "signal": [model, ds]
            }
        },
        "backtest": {
            "start_time": "2020-01-01",
            "end_time": "2020-03-31",
            "account": 100000000,
            "benchmark": ['SH601288'],
            "exchange_kwargs": {
                "freq": "day",
                "limit_threshold": 0.095,
                "deal_price": "close",
                "open_cost": 0.0005,
                "close_cost": 0.0015,
                "min_cost": 5,
            },
        },
    }

    ## backtest and analysis
    #with R.start(experiment_name="backtest_analysis"):
    #    recorder = R.get_recorder()

    #    sr = SignalRecord(model, ds, recorder)
    #    sr.generate()
    #    # backtest & analysis
    #    par = PortAnaRecord(recorder, port_analysis_config, "day")
    #    par.generate()
    # strategy object
    strategy_obj = VolumeStrategy(signal=[model, ds])
    EXECUTOR_CONFIG = {
        "time_per_step": "day",
        "generate_portfolio_metrics": True,
    }
    # executor object
    executor_obj = executor.SimulatorExecutor(**EXECUTOR_CONFIG)
    # backtest
    portfolio_metric_dict, indicator_dict = backtest(executor=executor_obj, strategy=strategy_obj, **port_analysis_config["backtest"])
    analysis_freq = "{0}{1}".format(*Freq.parse("day"))
    print("Freq.parse(\"day\"):", Freq.parse("day"))
    print("analysis_freq:", analysis_freq)
    # backtest info
    report_normal_df, positions_normal = portfolio_metric_dict.get(analysis_freq)
    print("report_normal_df:", report_normal_df)
    print("positions_normal:", positions_normal)
    print("qcr.GRAPH_NAME_LIST:", qcr.GRAPH_NAME_LIST)
    fig_list = analysis_position.report_graph(report_normal_df, show_notebook=False)
    for fig in fig_list:
        fig.show()


if __name__ == '__main__':
    provider_uri = '/Users/zhangyunsheng/Dev/sonata/data/qlib'  # target_dir
    qlib.init(provider_uri=provider_uri, region=REG_CN)

    ## 初始化的过程中已经完成的数据的load
    #volume_feature = VolumeFeature(instruments=['SH600006'], start_time='20180101', end_time='20200101')
    ##volume_feature = VolumeFeature(instruments='csi100', start_time='20180101', end_time='20200101')
    #data = volume_feature.fetch()
    ##print(data)
    #data.to_csv("/Users/zhangyunsheng/Dev/sonata/data/analysis/change",  sep='\t')
    #X = data['VOLUME_MEAN'].values
    #Y = data['LABEL'].values
    #plt.scatter(X, Y, 0.1, 'r')
    #plt.show()

    TopkDropoutStrategy

    analysis()
