#!/usr/bin/env python3
"""
通用爬虫 - 北京钟点工价格采集
支持：小红书、58同城、赶集网
"""
import json
import csv
import re
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import pandas as pd

class PriceCrawler:
    def __init__(self):
        self.results = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def crawl_xiaohongshu(self):
        """爬取小红书"""
        print("="*60)
        print("正在爬取小红书...")
        print("="*60)
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = context.new_page()
                
                # 搜索关键词
                keywords = ['北京钟点工价格', '北京保姆价格', '北京家政价格']
                
                for keyword in keywords:
                    print(f"\n搜索: {keyword}")
                    url = f'https://www.xiaohongshu.com/search_result?keyword={keyword}'
                    page.goto(url, wait_until='networkidle', timeout=60000)
                    time.sleep(5)
                    
                    # 获取内容
                    text = page.evaluate('() => document.body.innerText')
                    
                    # 提取价格
                    prices = re.findall(r'(\d{2,3})\s*元?[/小时h]', text)
                    for price in set(prices[:10]):
                        self.results.append({
                            'platform': '小红书',
                            'keyword': keyword,
                            'price': int(price),
                            'unit': '元/小时',
                            'crawl_time': datetime.now().isoformat()
                        })
                        print(f"  ✓ {price}元/小时")
                
                browser.close()
                
        except Exception as e:
            print(f"❌ 小红书爬取失败: {e}")
    
    def crawl_58com(self):
        """爬取58同城"""
        print("\n" + "="*60)
        print("正在爬取58同城...")
        print("="*60)
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                
                # 访问钟点工页面
                page.goto('https://bj.58.com/zhongdiangong/', 
                         wait_until='networkidle', timeout=60000)
                time.sleep(5)
                
                text = page.evaluate('() => document.body.innerText')
                
                # 提取价格
                prices = re.findall(r'(\d{2,3})\s*元?[/小时h]', text)
                for price in set(prices[:15]):
                    self.results.append({
                        'platform': '58同城',
                        'keyword': '钟点工',
                        'price': int(price),
                        'unit': '元/小时',
                        'crawl_time': datetime.now().isoformat()
                    })
                    print(f"  ✓ {price}元/小时")
                
                browser.close()
                
        except Exception as e:
            print(f"❌ 58同城爬取失败: {e}")
    
    def crawl_ganji(self):
        """爬取赶集网"""
        print("\n" + "="*60)
        print("正在爬取赶集网...")
        print("="*60)
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                
                page.goto('https://bj.ganji.com/zhongdiangong/',
                         wait_until='networkidle', timeout=60000)
                time.sleep(5)
                
                text = page.evaluate('() => document.body.innerText')
                
                prices = re.findall(r'(\d{2,3})\s*元?[/小时h]', text)
                for price in set(prices[:15]):
                    self.results.append({
                        'platform': '赶集网',
                        'keyword': '钟点工',
                        'price': int(price),
                        'unit': '元/小时',
                        'crawl_time': datetime.now().isoformat()
                    })
                    print(f"  ✓ {price}元/小时")
                
                browser.close()
                
        except Exception as e:
            print(f"❌ 赶集网爬取失败: {e}")
    
    def analyze(self):
        """分析结果"""
        print("\n" + "="*60)
        print("数据分析")
        print("="*60)
        
        if not self.results:
            print("❌ 没有获取到数据")
            return
        
        df = pd.DataFrame(self.results)
        
        print(f"\n总计: {len(self.results)} 条数据")
        print(f"\n按平台统计:")
        print(df.groupby('platform')['price'].agg(['count', 'mean', 'min', 'max']))
        
        print(f"\n整体统计:")
        print(f"  最低: {df['price'].min()} 元/小时")
        print(f"  最高: {df['price'].max()} 元/小时")
        print(f"  平均: {df['price'].mean():.1f} 元/小时")
        print(f"  中位: {df['price'].median():.1f} 元/小时")
        
        return df
    
    def save(self):
        """保存结果"""
        import os
        os.makedirs('data', exist_ok=True)
        
        # JSON
        json_file = f'data/prices_{self.timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ JSON 保存: {json_file}")
        
        # CSV
        if self.results:
            csv_file = f'data/prices_{self.timestamp}.csv'
            df = pd.DataFrame(self.results)
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"✅ CSV 保存: {csv_file}")
            
            # 汇总文件
            summary_file = 'data/latest_summary.csv'
            summary = df.groupby('platform')['price'].agg(['count', 'mean', 'min', 'max']).reset_index()
            summary.columns = ['平台', '样本数', '平均价格', '最低价格', '最高价格']
            summary.to_csv(summary_file, index=False, encoding='utf-8-sig')
            print(f"✅ 汇总保存: {summary_file}")
    
    def run(self):
        """运行所有爬虫"""
        print("🚀 开始爬取北京钟点工价格数据...\n")
        
        self.crawl_xiaohongshu()
        self.crawl_58com()
        self.crawl_ganji()
        
        self.analyze()
        self.save()
        
        print("\n✅ 完成!")

if __name__ == '__main__':
    crawler = PriceCrawler()
    crawler.run()
