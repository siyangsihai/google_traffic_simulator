#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
谷歌搜索流量模拟系统 (2025版)
主执行入口
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime

from src.browser_manager import BrowserManager
from src.action_simulator import ActionSimulator
from src.config_loader import ConfigLoader
from src.utils import setup_logging, rotate_proxy


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='谷歌搜索流量模拟系统')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--config', type=str, default='config/general.ini', help='配置文件路径')
    return parser.parse_args()


def main():
    """主程序入口"""
    args = parse_arguments()
    
    # 设置日志
    log_level = logging.DEBUG if args.debug else logging.INFO
    log_file = os.path.join('logs', f'traffic_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    logger = setup_logging(log_level, log_file)
    
    logger.info("谷歌搜索流量模拟系统启动")
    
    try:
        # 加载配置
        config_loader = ConfigLoader(args.config)
        config = config_loader.load_config()
        
        # 初始化浏览器管理器
        browser_manager = BrowserManager(config)
        
        # 初始化行为模拟器
        action_simulator = ActionSimulator(config)
        
        # 执行流量模拟
        visits = 0
        start_time = time.time()
        max_visits = config.getint('Browser', 'max_visits_per_hour')
        
        while visits < max_visits:
            # 获取代理
            #proxy = rotate_proxy(config_loader.load_proxies())
            #if not proxy:
            #    logger.error("没有可用的代理IP，暂停10分钟后重试")
            #    time.sleep(600)
            #    continue
            
            proxy = '127.0.0.1:7899'  # 使用本机代理
            # proxy = None  # 不使用任何代理
                
            # 创建浏览器实例
            driver = browser_manager.create_browser(proxy)
            
            try:
                # 随机选择关键词
                keyword = config_loader.get_random_keyword()
                logger.info(f"使用关键词: {keyword}")
                
                # 执行搜索
                action_simulator.google_search(driver, keyword)
                
                # 点击目标链接
                target_sites = config_loader.load_target_sites()
                clicked = action_simulator.click_target_links(driver, target_sites)
                
                if clicked:
                    logger.info("成功点击目标网站链接")
                else:
                    logger.warning("未找到匹配的目标网站链接")
                    
                visits += 1
                logger.info(f"完成第 {visits}/{max_visits} 次访问")
                
                # 计算下次访问延迟
                remaining_time = 3600 - (time.time() - start_time)
                if remaining_time <= 0 or visits >= max_visits:
                    # 重置计时器和访问计数
                    start_time = time.time()
                    visits = 0
                    logger.info("重置访问计数和计时器")
                    continue
                    
                delay = action_simulator.calculate_delay(remaining_time, max_visits - visits)
                logger.info(f"等待 {delay:.2f} 秒后进行下一次访问")
                time.sleep(delay)
                
            except Exception as e:
                logger.error(f"执行过程中出错: {str(e)}")
            finally:
                # 关闭浏览器
                browser_manager.close_browser(driver)
    
    except KeyboardInterrupt:
        logger.info("用户中断，正在退出...")
    except Exception as e:
        logger.critical(f"系统错误: {str(e)}")
    finally:
        logger.info("谷歌搜索流量模拟系统已停止")


if __name__ == "__main__":
    # 确保日志目录存在
    os.makedirs('logs', exist_ok=True)
    main()