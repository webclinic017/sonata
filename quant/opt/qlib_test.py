
import sys
import os
import pandas
import qlib
from qlib.data.dataset.loader import QlibDataLoader
from qlib.data.dataset.loader import StaticDataLoader
from qlib.data.dataset.handler import DataHandlerLP
from qlib.data.dataset.processor import CSZScoreNorm, DropnaProcessor, ZScoreNorm
from qlib.data.dataset import DatasetH
from qlib.data.dataset import TSDatasetH
from qlib.utils import init_instance_by_config
# region in [REG_CN, REG_US]
from qlib.config import REG_CN
from qlib.contrib.data.handler import Alpha158
from qlib.contrib.model.pytorch_alstm_ts import ALSTM
from qlib.workflow import R
from qlib.workflow.record_temp import SignalRecord, PortAnaRecord
from qlib.contrib.report import analysis_model, analysis_position
import torch
from torch.utils.tensorboard import SummaryWriter
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quotation.quotation import Quotation


def test():
    ### QlibDataLoader
    provider_uri = '/Users/zhangyunsheng/Dev/sonata/data/qlib'  # target_dir
    qlib.init(provider_uri=provider_uri, region=REG_CN)
    qdl = QlibDataLoader(config=(['$close', '$high'], ['close', 'high']))
    #d = qdl.load(instruments=['000001'], start_time='20210101', end_time='20230101')
    #print(d)
    ## 指数数据，多线程加载必须放在if __name__ == '__main__': 内
    d = qdl.load(instruments='csitest', start_time='20180101', end_time='20180107')
    print(d)

    ## StaticDataLoader
    #provider_uri = '/Users/zhangyunsheng/Dev/sonata/data/daily'  # target_dir
    #qlib.init(provider_uri=provider_uri, region=REG_CN)
    #sdl_csv = StaticDataLoader('/Users/zhangyunsheng/Dev/sonata/data/daily/000001.csv')
    #d = sdl_csv.load() # error
    #print(d)
    ##
    #q = Quotation()
    #df = q.get_daily_data('000001')
    #sdl_df = StaticDataLoader(config=df)
    #d = sdl_df.load()
    #print(d)

    ## Data Handler
    qdl = QlibDataLoader(config=(['$close/Ref($close, 1)-1'], ['Return']))
    d = qdl.load(instruments=['SZ000001'], start_time='20180101', end_time='20200101')
    # 是否有空值
    d.isna().sum()
    # 原始数据分布
    d.xs('2019-01-04').hist()
    # 分别定义shared_processors, learn_processors, infer_processors
    shared_processors = [DropnaProcessor()]
    learn_processors = [CSZScoreNorm()]
    infer_processors = [ZScoreNorm(fit_start_time='20180101', fit_end_time='20200101')]
    dh = DataHandlerLP(instruments=['SZ000001'], start_time='20180101', end_time='20200101',
                       process_type=DataHandlerLP.PTYPE_I,
                       learn_processors=learn_processors,
                       shared_processors=shared_processors,
                       infer_processors=infer_processors,
                       data_loader=qdl)
    #df_hdl = dh.fetch(data_key=DataHandlerLP.DK_I)
    #print(df_hdl)
    df_hdl = dh.fetch(data_key=DataHandlerLP.DK_L)
    #print(df_hdl)
    # 查看是否还存在空值
    df_hdl.isna().sum()
    # CSZScoreNorm截面标准化处理后的数据分布
    d.xs('2019-01-04').hist()
    # 原始数据
    raw_df = dh.fetch(data_key=DataHandlerLP.DK_R)
    # 处理后的数据
    infer_df = dh.fetch(data_key=DataHandlerLP.DK_I)
    learn_df = dh.fetch(data_key=DataHandlerLP.DK_L) # ?数据Na
    #print(raw_df)
    #print(infer_df)
    #print(learn_df)

    ## Dataset
    ds = DatasetH(dh, segments={'train': ('20180101', '20181231'), 'test': ('20190101', '20191231')})
    # 准备训练数据
    ds.prepare('train')
    # 准备测试数据
    ds.prepare('test')


    ## config
    qdl_config = {
        'class' : 'QlibDataLoader',
        'module_path' : 'qlib.data.dataset.loader',
        'kwargs' : {
            'config' : {
                'feature': (['EMA($close, 10)', 'EMA($close, 30)'], ['EMA10', 'EMA30']),
                'label': (['Ref($close, -1)/$close - 1', ], ['RET_1', ]),
            },
            'freq': 'day',
        }
    }
    qdl = init_instance_by_config(qdl_config)
    d = qdl.load(instruments=['SZ000001'], start_time='20180101', end_time='20200101')
    #print(d)


# 实现一个自定义的特征集，MACD、RSI
class MyFeatureSet(DataHandlerLP):
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
        MACD = '(EMA($close, 12) - EMA($close, 26))/$close - EMA((EMA($close, 12) - EMA($close, 26))/$close, 9)/$close'
        RSI = '100 - 100/(1+(Sum(Greater($close-Ref($close, 1),0), 14)/Count(($close-Ref($close, 1))>0, 14))/ (Sum(Abs(Greater(Ref($close, 1)-$close,0)), 14)/Count(($close-Ref($close, 1))<0, 14)))'

        return [MACD, RSI, '$open', '$close', '$high', '$low', '$change'], ['MACD', 'RSI', 'open', 'close', 'high', 'low', 'change']

    def get_label_config(self):
        return (['Ref($close, -1)/$close - 1'], ['LABEL'])

def train():
    train_period = ('2015-01-01', '2015-03-31')
    valid_period = ('2019-01-01', '2019-03-31')
    test_period = ('2020-01-01', '2020-03-31')

    dh = Alpha158(instruments=['SH600006'],
                  start_time=train_period[0],
                  end_time=test_period[1],
                  inst_processor={}
                  )

    ds = TSDatasetH(
        handler=dh,
        step_len=40,
        segments={
            'train': train_period,
            'valid': valid_period,
            'test': test_period
        }
    )

    model = ALSTM(d_feat=158,
              metric='',
              rnn_type='GRU',
              batch_size=800,
              early_stop=10,
              n_epochs=1
             )   # 其他参数使用默认设置

    model_path = os.path.dirname(os.path.abspath(__file__)) + '/../../data/model/test_qlib_model.zip'
    model_path_pkl = os.path.dirname(os.path.abspath(__file__)) + '/../../data/model/test_qlib_model.pkl'
    print(model_path)
    experiment_name = 'train_model'
    #if os.path.exists(model_path):
    #    best_param = torch.load(model_path)
    #    model.ALSTM_model.load_state_dict(best_param)
    #    model.fitted = True
    #else:
    #    model.fit(dataset=ds, save_path=model_path)

    if os.path.exists(model_path_pkl):
        model.load(model_path_pkl)
        model.fitted = True
    else:
        with R.start(experiment_name=experiment_name):
            model.fit(dataset=ds, save_path=model_path)
            #R.save_objects(**{'test_qlib_model.pkl': model}, artifact_path='artifact_path')
            R.save_objects(**{model_path_pkl: model}, artifact_path='artifact_path')
            rid = R.get_recorder().id
            print(rid)

    #with R.start(experiment_name='backtest_analysis'):
    #    recorder = R.get_recorder(recorder_id='cbd99b0fbcf74fdeaa51889972ef534c', experiment_name=experiment_name)
    #    model = recorder.load_object('artifact_path/test_qlib_model.pkl')

    #    # prediction
    #    recorder = R.get_recorder()
    #    ba_rid = recorder.id
    #    print('ba_rid', ba_rid)
    #    sr = SignalRecord(model, ds, recorder)
    #    sr.generate()

    #    ## backtest & analysis
    #    #par = PortAnaRecord(recorder, port_analysis_config, 'day')
    #    #par.generate()

    p = model.predict(dataset=ds, segment='test')
    print(p)

    ### 如何使用Tensorboard查看模型结构
    #writer = SummaryWriter(os.path.dirname(os.path.abspath(__file__)) + '/../../data/model/test_qlid_model.sum')
    #writer.add_graph(model, model.ALSTM_model.state_dict()) # ModuleNotFoundError: No module named 'caffe2'
    #writer.close()
    ## 在终端中运行(当前文件夹)以下命令，会有如下输出，然后再在浏览器打开localhost:6006
    ## tensorboard --logdir='./runs'

def train_by_config():
    ds_config = {
        'class': 'TSDatasetH',
        'module_path': 'qlib.data.dataset',
        'kwargs': {
            'handler': {
                'class': 'Alpha158',
                'module_path': 'qlib.contrib.data.handler',
                'kwargs': {
                    'start_time': '2015-01-01',
                    'end_time': '2020-03-31',
                    'fit_start_time': '2015-01-01',
                    'fit_end_time': '2019-03-31',
                    'instruments': ['SH600006'],
                    # 与之前的示例相比，这里新增了infer_processors和learn_processors
                    'infer_processors': [
                        {'class': 'RobustZScoreNorm',
                         'kwargs': {'fields_group': 'feature', 'clip_outlier': True}},
                        {'class': 'Fillna', 'kwargs': {'fields_group': 'feature'}}],
                    'learn_processors': [{'class': 'DropnaLabel'},
                                         # 对预测的目标进行截面排序处理
                                         {'class': 'CSRankNorm', 'kwargs': {'fields_group': 'label'}}],
                    # 预测的目标
                    'label': ['Ref($close, -1) / $close - 1']
                }
            },
            'segments': {'train': ["2015-01-01", "2015-03-31"],
                         'valid': ['2019-01-01', '2019-03-31'],
                         'test': ['2020-01-01', '2020-03-31']},
            'step_len': 40
        }
    }
    model_config = {'class': 'ALSTM',
                    'module_path': 'qlib.contrib.model.pytorch_alstm_ts',
                    'kwargs': {
                        'd_feat': 158,
                        'hidden_size': 64,
                        'num_layers': 2,
                        'dropout': 0.0,
                        'n_epochs': 1,
                        'lr': 1e-3,
                        'early_stop': 10,
                        'batch_size': 800,
                        'metric': 'loss',
                        'loss': 'mse',
                        'n_jobs': 20,
                        'GPU': 0,
                        'rnn_type': 'GRU'
                    }}
    ds = init_instance_by_config(ds_config)
    print(ds.handler)
    model = init_instance_by_config(model_config)
    model.fit(dataset=ds)


def analysis():
    #  jupyter notebook
    print(R.list_experiments())  # 列出当前所有experiments

    recorder = R.get_recorder(recorder_id='31725e5e58604722830111d4c7c6b53a', experiment_name='workflow')

    # 预测结果
    pred_df = recorder.load_object("pred.pkl")
    # RankIc序列
    print(recorder.load_object('sig_analysis/ric.pkl'))
    # 回测报告（净值，交易成本等）
    report_normal_df = recorder.load_object("portfolio_analysis/report_normal_1day.pkl")

    analysis_df = recorder.load_object("portfolio_analysis/port_analysis_1day.pkl")
    positions = recorder.load_object("portfolio_analysis/positions_normal_1day.pkl")

    analysis_position.report_graph(report_normal_df)
    # risk analysis
    analysis_position.risk_analysis_graph(analysis_df, report_normal_df)





if __name__ == '__main__':
    provider_uri = '/Users/zhangyunsheng/Dev/sonata/data/qlib'  # target_dir
    qlib.init(provider_uri=provider_uri, region=REG_CN)

    #test()

    #provider_uri = '/Users/zhangyunsheng/Dev/sonata/data/qlib'  # target_dir
    #qlib.init(provider_uri=provider_uri, region=REG_CN)
    # 初始化的过程中已经完成的数据的load
    my_feature = MyFeatureSet(instruments=['SH600006'], start_time='20180101', end_time='20200101')
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.max_rows', None)
    print(my_feature.fetch().head(50))

    #train()

    #train_by_config()

    #analysis()





