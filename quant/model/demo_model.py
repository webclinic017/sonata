#!/usr/bin/python
#-*- coding: utf-8 -*-

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

from .gym_env.stock_trade_env import StockTradingEnv
from .base_model import BaseModel
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import utils.const as CT
from utils.logger import Logger
from quotation.quotation import Quotation


class DemoModel(BaseModel):
    model_name = 'demo'
    model_dir = CT.MODEL_DIR + model_name
    model = None

    def __init__(self):
        return

    def train(self):
        q = Quotation()
        d = q.get_daily_data('000001')
        d = d.reset_index()
        # d = pd.read_csv('/Users/zhangyunsheng/Dev/sonata/data/AAPL.csv')
        d = d.sort_values('date')

        # The algorithms require a vectorized environment to run
        env = DummyVecEnv([lambda: StockTradingEnv(d)])

        #m = PPO2(MlpPolicy, env, verbose=1)
        #m.learn(total_timesteps=20000)
        #m.save(self.model_dir)

        m = PPO2.load(self.model_dir)
        obs = env.reset()
        for i in range(2000):
            action, _states = m.predict(obs)
            print(action) # TODO
            if action[0][0] < 1:
                if action[0][1] != 0:
                    print('BUY')  # TODO
            elif action[0][0] < 2:
                if action[0][1] != 0:
                    print('SELL')  # TODO
            obs, rewards, done, info = env.step(action)
            env.render()
        return True

    def load(self):
        try:
            q = Quotation()
            d = q.get_daily_data('000001')
            d = d.reset_index()
            # d = pd.read_csv('/Users/zhangyunsheng/Dev/sonata/data/AAPL.csv')
            d = d.sort_values('date')
            env = DummyVecEnv([lambda: StockTradingEnv(d)])
            self.model = PPO2(MlpPolicy, env, verbose=1)
            self.model = PPO2.load(self.model_dir)
        except Exception as e:
            Logger.warn(e)
            return False
        return True

    def predict(self, code):
        if self.model == None:
            self.load()
        q = Quotation()
        d = q.get_daily_data(code)
        d = d.reset_index()
        n = len(d.loc[:, 'open'].values)
        last_five_d = d.loc[n - 6:, :]
        obs = StockTradingEnv.observation(last_five_d)
        action, _states = self.model.predict(obs)
        print(action)
        print(_states)
        return

def main(argv):
    m = DemoModel()
    m.train()
    #m.load()
    #m.predict('000001')

if __name__ == "__main__":
    main(sys.argv)
