#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""行为模拟器模块"""

import random
import re
import time
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ActionSimulator:
    """行为模拟器类"""
    
    def __init__(self, config):
        """初始化行为模拟器"""
        self.config = config
        self.min_delay = config.getint('Behavior', 'min_delay')
        self.max_delay = config.getint('Behavior', 'max_delay')
    
    def random_delay(self):
        """随机延迟"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
    
    def google_search(self, driver, keyword):
        """执行谷歌搜索"""
        driver.get('https://www.google.com')
        self.random_delay()
        
        # 定位搜索框并输入关键词
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_box.clear()
        search_box.send_keys(keyword)
        self.random_delay()
        search_box.send_keys(Keys.RETURN)
        
        # 等待搜索结果加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search'))
        )
        self.random_delay()
    
    def click_target_links(self, driver, target_sites):
        """点击目标网站链接"""
        # 获取所有搜索结果链接
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#search a'))
        )
        
        # 过滤匹配目标网站的链接
        target_links = []
        for link in search_results:
            try:
                href = link.get_attribute('href')
                if href and not href.startswith('https://www.google.com'):
                    domain = urlparse(href).netloc
                    for pattern in target_sites:
                        if re.search(pattern, domain):
                            target_links.append(link)
                            break
            except Exception:
                continue
        
        if not target_links:
            return False
        
        # 随机选择一个目标链接点击
        target_link = random.choice(target_links)
        driver.execute_script("arguments[0].click();", target_link)  # 使用JavaScript点击
        self.random_delay()
        
        # 增加随机停留时间
        stay_time = random.uniform(10, 20)
        time.sleep(stay_time)
        
        return True
    
    def calculate_delay(self, remaining_time, remaining_visits):
        """计算下次访问延迟"""
        if remaining_visits <= 0:
            return 0
        
        # 计算平均每次访问需要的时间
        avg_time_per_visit = remaining_time / remaining_visits
        
        # 在平均时间基础上增加随机波动
        min_delay = max(self.min_delay, avg_time_per_visit * 0.8)
        max_delay = min(self.max_delay, avg_time_per_visit * 1.2)
        
        return random.uniform(min_delay, max_delay)