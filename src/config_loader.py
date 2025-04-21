#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""配置加载器
负责加载和解析配置文件，包括general.ini、keywords.txt和sites.txt
"""

import configparser
import os
import random

class ConfigLoader:
    def __init__(self, config_file):
        """初始化配置加载器
        
        Args:
            config_file: 主配置文件路径
        """
        self.config_file = config_file
        self.config_dir = os.path.dirname(config_file)
        
    def load_config(self):
        """加载主配置文件
        
        Returns:
            configparser.ConfigParser: 配置对象
        """
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config
        
    def get_random_keyword(self):
        """随机获取一个搜索关键词
        
        Returns:
            str: 搜索关键词
        """
        keywords = []
        keywords_file = os.path.join(self.config_dir, 'keywords.txt')
        
        with open(keywords_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    keywords.append(line)
                    
        return random.choice(keywords) if keywords else ''
        
    def load_target_sites(self):
        """加载目标网站列表
        
        Returns:
            list: 目标网站域名列表
        """
        sites = []
        sites_file = os.path.join(self.config_dir, 'sites.txt')
        
        with open(sites_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    sites.append(line)
                    
        return sites
        
    def load_proxies(self):
        """加载代理IP列表（示例方法）
        
        Returns:
            list: 代理IP列表
        """
        # TODO: 实现从代理服务商API获取代理IP
        return ['127.0.0.1:8080']  # 示例代理