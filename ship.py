# coding=utf-8

import pygame

class Ship():
	def __init__(self,screen,ai_settings):
		"""初始化飞船并设置其初始化位置"""
		self.screen=screen
		self.ai_settings=ai_settings
		
		# 加载飞船图像并获取其外接矩形
		self.image=pygame.image.load('images/ship.bmp')
		self.rect=self.image.get_rect()
		self.screen_rect=self.screen.get_rect()
		
		# 将每艘飞船都放在屏幕的底部中央
		self.rect.centerx=self.screen_rect.centerx
		self.rect.bottom=self.screen_rect.bottom
		
		# 存储飞船位置的小数值
		self.center=float(self.rect.centerx)
		
		# 移动标志
		self.moving_right=False
		self.moving_left=False
		
	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image,self.rect)
		
	def update(self):
		"""根据移动的标志调整飞船的位置"""
		
		# 更新飞船center，注意不是rect
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.center+=self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left>0:
			self.center-=self.ai_settings.ship_speed_factor
		
		# 根据飞船的center更新rect对象
		self.rect.centerx=self.center
		
