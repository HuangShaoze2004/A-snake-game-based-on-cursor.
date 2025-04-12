# 贪吃蛇游戏

一个使用Python和Pygame库开发的现代贪吃蛇游戏，具有丰富的视觉效果和音效。

## 功能特色

- 精美的游戏界面与动画效果
- 完整的音效系统（吃食物、游戏结束、菜单选择等）
- 三种游戏难度可选（简单、中等、困难）
- 特殊食物系统（金色食物提供额外分数和长度）
- 渐变色彩的蛇身效果
- 游戏结束菜单与分数显示

## 安装依赖

在运行游戏前，请确保安装了所需的依赖：

```
pip install pygame numpy scipy
```

## 游戏控制

- 使用方向键（上、下、左、右）控制蛇的移动
- 吃普通食物（红色）增加蛇的长度和1分
- 吃特殊食物（金色闪烁）增加蛇的长度2格并获得3分
- 撞到墙壁或自己的身体会导致游戏结束
- 游戏结束后，可以选择重新开始或返回主菜单

## 游戏难度

- 简单：较慢的初始速度，适合新手
- 中等：中等初始速度，提供平衡的游戏体验
- 困难：较快的初始速度，具有挑战性

## 分数系统

- 游戏会记录你吃食物的得分
- 每吃5个食物会提高游戏速度，增加难度
- 游戏结束时会显示最终得分

## 运行游戏

```
python Snake Game.py
```

祝你游戏愉快！

## 开发者

设计与开发：HuangShaoze 