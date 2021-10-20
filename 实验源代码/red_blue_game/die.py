#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Site    : 
# @File    : die.py
"""
用两个骰子来简单模拟红蓝博弈，取消交流环节
居中人：骰子，随机抛掷，1、3、5则为合作，2、4、6为背叛
奖罚规则：都合作各加3，都背叛各罚3，其余背叛加6合作减6
博弈轮次：1、2、4、5正常奖罚，3、6双倍奖罚，7、8平方倍赏罚（-3平方为-9）
"""

import random

die_2_bool = {1: True, 3: True, 5: True, 2: False, 4: False, 6: False}  # 用布尔值来转化投掷结果
SEED = 3  # 这是奖罚基数
# 把局中人的对策映射到得分结果
decision_2_score = {
    (True, True): [3, 3],
    (False, False): [-3, -3],
    (True, False): [-6, 6],
    (False, True): [6, -6]
}


class Player:
    # 只有一个分数属性和决策方法
    def __init__(self):
        self.score = 0  # 用来记录分数

    @property
    def decision(self):
        decision = die_2_bool[random.randint(1, 6)]
        return decision  # 返回决策结果，True-->合作， False-->背叛


class Game:
    # 组织一局博弈游戏，一局游戏默认局中人博弈8轮
    def __init__(self, *players, rounds=8):
        self.rounds = rounds  # 回合数
        self.players = players  # 需要两个局中人
        self.record = {"rounds": {}, "fin_score": 0}  # 单局博弈总记录
        self.is_clean = True  # 是否清理好并可以开始下一局博弈

    def decide(self):
        # 返回一轮博弈中所有剧中人的决策结果
        decisions = []
        for player in self.players:
            decisions.append(player.decision)
        return decisions

    def exe(self):
        # 进行一局多轮博弈
        if self.is_clean:
            # 必须有此步，否则无法重复正常模拟
            self.is_clean = False
        else:
            exit()
        #开始每一轮的博弈并进行记录
        for round in range(1, self.rounds + 1):
            decisions = self.decide() #搜集本轮玩家策略
            changed = self.punish_or_reward(decisions, round) #根据双方策略和轮次进行奖惩
            #进行记录游戏数据
            self.record["rounds"][round] = {
                "decisions": decisions,
                "changed": changed}
            if round == self.rounds:
                #最后一轮结束后纪录最终得分
                self.record["fin_score"] = [player.score for player in self.players]
        record = self.record
        self.clean()
        return record

    def clean(self):
        # 一局博弈结束，清仓大处理，重置选手状态
        self.record = {"rounds": {}, "fin_score": 0}  # 重置记录
        for i in range(2): self.players[i].score = 0
        self.is_clean = True

    def change_score(self, round, score):
        # 根据当前轮数来改变奖罚基数
        if round in [1, 2, 4, 5]:
            score = score
        elif round in [3, 6]:
            score = [sco * 2 for sco in score]
        else:
            score = [sco / abs(sco) * pow(sco, 2) for sco in score]
        return score

    def punish_or_reward(self, decisions, round):
        decisions = tuple(decisions)
        score = decision_2_score[decisions]
        score = self.change_score(round, score)
        for i in range(2):
            self.players[i].score += score[i]
        return score
