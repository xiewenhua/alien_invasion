# coding=utf-8

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
	# 初始化游戏并创建一个屏幕对象
	pygame.init()
	ai_settings=Settings()
	screen=pygame.display.set_mode(
		(ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("外星人入侵")
	
	# 创建一个用于存储游戏统计信息的实例，并创建一个记分牌
	stats=GameStats(ai_settings)
	sb=Scoreboard(ai_settings,screen,stats)
	
	#创建一艘飞船、一个子弹编组和一个外星人编组
	ship=Ship(screen,ai_settings)
	bullets=Group()
	aliens=Group()
	
	# 创建外星人群
	gf.create_fleet(ai_settings,screen,aliens,ship)
	
	# 创建Play按钮
	play_button=Button(ai_settings,screen,"Play")
	
	
	# 开始游戏主循环
	while True:
		gf.check_events(sb,aliens,ai_settings,ship,bullets,screen,stats,play_button)
		if stats.game_active:
			ship.update()
			gf.update_bullets(stats,sb,bullets,ai_settings,screen,aliens,ship)
			gf.update_aliens(sb,stats,aliens,bullets,ai_settings,screen,ship)
		gf.update_screen(sb,stats,aliens,screen,ship,ai_settings,bullets,play_button)
		
run_game()

