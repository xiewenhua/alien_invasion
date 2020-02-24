# coding=utf-8

import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(stats,ai_settings,screen,event,ship,bullets):
	"""相应按键"""
	if event.key==pygame.K_q:
		sys.exit()
	elif event.key==pygame.K_RIGHT:
		ship.moving_right=True
	elif event.key==pygame.K_LEFT:
		ship.moving_left=True
	elif event.key==pygame.K_SPACE and stats.game_active:
		fire_bullet(bullets,ship,screen,ai_settings)

def fire_bullet(bullets,ship,screen,ai_settings):
	"""如果还没有达到子弹数量上限，那就发射一颗子弹"""
	# 创建一颗子弹，并将其加入到编组bullets中
	if len(bullets)<3:
		new_bullet=Bullet(ship,screen,ai_settings)
		bullets.add(new_bullet)
					
def check_keyup_events(event,ship):
	"""相应松开按键"""
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False	

def check_events(sb,aliens,ai_settings,ship,bullets,screen,stats,play_button):
	# 监视键盘和鼠标事件
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(stats,ai_settings,screen,event,ship,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type==pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y=pygame.mouse.get_pos()
			check_play_button(sb,ship,screen,ai_settings,bullets,
				aliens,stats,play_button,mouse_x,mouse_y)
def check_play_button(sb,ship,screen,ai_settings,bullets,
	aliens,stats,play_button,mouse_x,mouse_y):
	"""点击Play按钮的时候响应处理"""
	button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)			
	if button_clicked and not stats.game_active:
		# 游戏开始，隐藏鼠标
		pygame.mouse.set_visible(False)
		
		# 重置游戏设置
		ai_settings.initialize_dynamic_settings()
		
		# 重置游戏统计信息
		stats.reset_stats()
		stats.game_active=True
		
		# 重置记分牌图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		# 情况外星人和子弹列表
		aliens.empty()
		bullets.empty()
		
		# 创建一群新的外星人，并让飞船居中
		create_fleet(ai_settings,screen,aliens,ship)
		ship.center_ship()
					
				
def update_screen(sb,stats,aliens,screen,ship,ai_settings,bullets,play_button):
	"""更新屏幕上的所有图像"""

	# 每次循环时都重绘屏幕
	screen.fill(ai_settings.bg_color)
	# 在外星人和飞船的后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	
	# 显示得分
	sb.show_score()
	
	# 如果游戏处于非活动状态，就绘制Play按钮
	if not stats.game_active:
		play_button.draw_button()
			
	# 让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(stats,sb,bullets,ai_settings,screen,aliens,ship):
	"""更新子弹的位置并删除已经消失的子弹"""
	bullets.update()
	
	# 删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)
			
	check_bullet_alien_collisions(stats,sb,bullets,ai_settings,screen,aliens,ship)		
			
def check_bullet_alien_collisions(stats,sb,bullets,ai_settings,screen,aliens,ship):
	"""响应子弹和外星人的碰撞"""
	# 检查是否又子弹击中了外星人
	# 如果是这样，就删除相应的子弹和外星人
	collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for aliens in collisions.values():
			stats.score+=ai_settings.alien_points*len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	
	if len(aliens)==0:
		# 删除现有的子弹并且创建新的外星人群
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings,screen,aliens,ship)
		stats.level+=1
		sb.prep_level()
		
	
def create_alien(ai_settings,screen,alien_number,row_number,aliens):
	"""创建一个外星人并将其放在当前行"""
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width+2*alien_width*alien_number
	alien.rect.x=alien.x
	alien.y=alien.rect.height+2*alien.rect.height*row_number
	alien.rect.y=alien.y
	aliens.add(alien)
	
def get_number_aliens_x(ai_settings,alien_width):
	"""算一行可以容纳多少个外星人"""		
	alienable_space_x=ai_settings.screen_width-2*alien_width
	number_aliens_x=int(alienable_space_x/(2*alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings,alien_height,ship_height):
	alienable_space_y=(ai_settings.screen_height
		-ship_height-(3*alien_height))
	number_rows=int(alienable_space_y/(2*alien_height))	
	return number_rows
	
def create_fleet(ai_settings,screen,aliens,ship):
	"""创建外星人群"""
	alien=Alien(ai_settings,screen)
	number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows=get_number_rows(ai_settings,alien.rect.height,ship.rect.height)
	# 创建第一行外星人
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,alien_number,row_number,aliens)
def check_aliens_bottom(sb,stats,aliens,bullets,ai_settings,screen,ship):
	"""检查是否又外星人到达了屏幕底部"""
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom>=screen_rect.bottom:
			# 撞到屏幕和撞到飞船的结果都是一样
			print("外星人已经入侵了")
			ship_hit(sb,stats,aliens,bullets,ai_settings,screen,ship)
			break
	
	
def update_aliens(sb,stats,aliens,bullets,ai_settings,screen,ship):
	check_fleet_edges(aliens,ai_settings)
	aliens.update()
	
	#检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		print("飞船撞到外星人了")
		ship_hit(sb,stats,aliens,bullets,ai_settings,screen,ship)
		
	check_aliens_bottom(sb,stats,aliens,bullets,ai_settings,screen,ship)
	
def ship_hit(sb,stats,aliens,bullets,ai_settings,screen,ship):
	"""响应外星人撞到飞船"""
	# 剩余飞船数量减1
	stats.ships_left-=1	
	# 更新记分牌
	sb.prep_ships()
	if stats.ships_left>0:	
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		
		# 创建新的外星人，并恢复飞船到初始位置
		create_fleet(ai_settings,screen,aliens,ship)
		ship.center_ship()
		
		# 暂停碰撞的屏幕
		sleep(0.5)
	else:
		print("游戏结束！\n")
		stats.game_active=False
		pygame.mouse.set_visible(True)

def check_fleet_edges(aliens,ai_settings):
	"""当检查到外星人群碰到屏幕边缘时改变外星人移动方向"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	"""让外星人群改变移动的方向，并且往下移"""
	for alien in aliens.sprites():
		alien.rect.y+=ai_settings.fleet_drop_speed
	ai_settings.fleet_direction*=-1

def check_high_score(stats,sb):
	"""检查是否诞生了新的最高得分"""
	if stats.score>stats.high_score:
		stats.high_score=stats.score
		sb.prep_high_score()
