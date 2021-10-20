#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Site    : 
# @File    : main.py
import os
from die import Player, Game
import dataProcessor as dp


def get_data(cwd,times=100):
    # 创造玩家和对局，准备收集数据
    p1 = Player()
    p2 = Player()
    game = Game(p1, p2)
    datas = {}
    # 默认收集100局博弈数据，并保存成json文件可供别人使用
    for i in range(1,times+1):
        datas[i] = game.exe()

    dp.store_2_json("\datas.json", cwd, datas)
    return datas


def process_data(datas,cwd,write_2_excel=True, render=True):
    if write_2_excel==True:
        render_data=dp.write_2_excel("\一半合作.xlsx",cwd,datas=datas,render=render)
        if render:
            dp.render("\离散型概率分布图.png",cwd,render_data=render_data)



if __name__ == '__main__':
    cwd = os.getcwd()
    datas=get_data(cwd,times=1000)  # 创造数据，调用一次产生100局的游戏数据
    process_data(datas=datas,cwd=cwd) # 处理数据，如写出excel，做出概率分布图

