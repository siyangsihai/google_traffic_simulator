#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
浏览器管理器
负责创建和管理浏览器实例
"""

import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from fake_useragent import UserAgent

class BrowserManager:
    def __init__(self, config):
        self.config = config
        self.user_agent = UserAgent()
        self.use_proxy = config.get('Browser', 'use_proxy', fallback=False)
        self.browser_weights = [int(w) for w in config.get('Browser', 'browser_weights', fallback='6,2,2').split(',')]
        self.browser_types = ['chrome', 'safari', 'edge']
        
    def create_browser(self, proxy=None):
        """创建浏览器实例"""
        # 根据权重随机选择浏览器类型
        browser_type = random.choices(self.browser_types, weights=self.browser_weights)[0]
        
        if browser_type == 'chrome':
            options = ChromeOptions()
            if self.config.getboolean('Browser', 'headless'):
                options.add_argument('--headless')
            if self.use_proxy and proxy:
                options.add_argument(f'--proxy-server={proxy}')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
        elif browser_type == 'safari':
            options = SafariOptions()
            service = SafariService()
            driver = webdriver.Safari(service=service, options=options)
            
        else:  # edge
            options = EdgeOptions()
            if self.config.getboolean('Browser', 'headless'):
                options.add_argument('--headless')
            if self.use_proxy and proxy and self.config.getboolean('Browser', 'use_proxy', fallback=True):
                options.add_argument(f'--proxy-server={proxy}')
            options.add_argument('--disable-gpu')
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
        
        # 设置随机屏幕分辨率
        width = random.randint(
            self.config.getint('Fingerprint', 'screen_min_width'),
            self.config.getint('Fingerprint', 'screen_max_width')
        )
        height = random.randint(
            self.config.getint('Fingerprint', 'screen_min_height'),
            self.config.getint('Fingerprint', 'screen_max_height')
        )
        driver.set_window_size(width, height)
        
        # 设置页面加载超时
        driver.set_page_load_timeout(self.config.getint('Proxy', 'timeout', fallback=30))
        driver.set_script_timeout(self.config.getint('Proxy', 'timeout', fallback=30))
        
        return driver
        
    def close_browser(self, driver):
        """关闭浏览器实例"""
        if driver:
            try:
                driver.quit()
            except Exception:
                pass