# coding=utf-8

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
	# 初始化游戏并创建一个屏幕对象
	pygame.init()
	ai_settings=Settings()
	screen=pygame.display.set_mode(
		(ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("外星人入侵")
	
	#创建一艘飞船、一个子弹编组和一个外星人编组
	ship=Ship(screen,ai_settings)
	bullets=Group()
	aliens=Group()
	
	# 创建外星人群
	gf.create_fleet(ai_settings,screen,aliens,ship)
	
	# 开始游戏主循环
	while True:
		gf.check_events(ai_settings,ship,bullets,screen)
		ship.update()
		gf.update_bullets(bullets,ai_settings,screen,aliens,ship)
		gf.update_aliens(aliens,ship,ai_settings)
		gf.update_screen(aliens,screen,ship,ai_settings,bullets)
		
run_game()

