#!/usr/bin/python
# coding:utf-8

import datetime
import backtrader as bt
import os.path
import sys

class MyPandasData(bt.feeds.PandasData):
    lines = ('turnover',)
    params = (('turnover', -1),)

class TestStrategy(bt.Strategy):
    params = (
        #('exitbars', 5),
        ('maperiod', 15),
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=True):
        dt = dt or self.datas[0].datetime.date(0)
        if doprint:
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        #self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)
        self.cmpval = self.data.close(-1)

        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def notify_order(self, order):
        self.log('notify_order，order:%s, 价格：%.2f, 费用： %.2f, 佣金: %.2f' %
                 (order,
                  order.executed.price,
                  order.executed.value,
                  order.executed.comm))
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('已买入， 价格：%.2f, 费用： %.2f, 佣金: %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            elif order.issell():
                self.log('已卖出， 价格：%.2f, 费用： %.2f, 佣金: %.2f' %
                     (order.executed.price,
                      order.executed.value,
                      order.executed.comm))
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('交易利润，毛利率：%.2f, 净利率：%.2f' %
                 (trade.pnl, trade.pnlcomm))


    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if not self.position:
            #if self.dataclose[0] < self.dataclose[-1]:
            #    if self.dataclose[-1] < self.dataclose[-2]:
            #        self.log('buy, %.2f' % self.dataclose[0])
            #        self.order = self.buy()
            if self.dataclose[0] > self.sma[0]:
                self.log('buy, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            #if len(self) >= self.bar_executed + self.params.exitbars:
            #    self.log('sell, %.2f' % self.dataclose[0])
            #    self.order = self.sell()
            if self.dataclose[0] < self.sma[0]:
                self.log('sell, %.2f' % self.dataclose[0])
                self.order = self.sell()

    def stop(self):
        self.log('(均线周期 %2d)期末资金 %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)

if __name__ == '__main__':
    #cerebro = bt.Cerebro()
    cerebro = bt.Cerebro(stdstats=False)

    cerebro.addstrategy(TestStrategy)
    #strats = cerebo.optstrategy(
    #    TestStrategy,
    #    maperiod=range(10, 31))

    # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, 'orcl-1995-2014.txt')
    # data = bt.feeds.YahooFinanceCSVData(
    #     dataname=datapath,
    #     fromdate=datetime.datetime(2000, 1, 1),
    #     todate=datetime.datetime(2000, 12, 31),
    #     reverse=False
    # )

    from quotation.quotation import Quotation
    q = Quotation()
    d = q.get_daily_data('000001')
    print(d)

    # import pandas
    # #d = pandas.read_csv(datapath, skiprows=0, parse_dates=True,  header=0, index_col=0)
    # datapath = "/Users/zhangyunsheng/Dev/sonata/data/daily/000001"
    # d = pandas.read_csv(datapath, sep='\t', skiprows=0, parse_dates=True,  header=0, index_col=0)
    # print(d)
    # exit()

    #data = bt.feeds.PandasData(
    #    dataname=d,
    #    fromdate=datetime.datetime(2001, 1, 1),
    #    todate=datetime.datetime(2001, 12, 31),
    #    )
    data = MyPandasData(
        dataname=d,
        fromdate=datetime.datetime(2001, 1, 1),
        todate=datetime.datetime(2001, 12, 31),
        )

    cerebro.adddata(data)


    cerebro.broker.setcash(1000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)
    print('Starting Protffolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Protffolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()

