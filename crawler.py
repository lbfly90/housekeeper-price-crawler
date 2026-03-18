#!/usr/bin/env python3
"""
通用爬虫 - 北京钟点工价格采集
支持：58同城、赶集网、美团、大众点评（使用 Jina AI 免费服务）
"""
import json
import csv
import re
import time
import requests
from datetime import datetime
from urllib.parse import quote

class PriceCrawler:
    def __init__(self):
        self.results = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.jina_base = "https://r.jina.ai/http://"
        
    def fetch_jina(self, url):
        """使用 Jina AI 免费服务抓取页面"""
        jina_url = f"{self.jina_base}{url}"
        try:
            response = requests.get(jina_url, timeout=30)
            if response.status_code == 200:
                return response.text
            else:
                print(f"  ⚠️ 状态码: {response.status_code}")
                return None
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")
            return None
    
    def extract_prices(self, text, platform):
        """从文本中提取价格"""
        # 匹配价格模式
        patterns = [
            r'(\d{2,3})\s*元?[/小时h]',
            r'(\d{2,3})\s*元',
            r'价格[:：]\s*(\d{2,3})',
            r'(\d{2,3})\s*元/小时',
            r'均价[:：]\s*(\d{2,3})',
            r'起价[:：]\s*(\d{2,3})',
        ]
        
        prices = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            prices.extend([int(m) for m in matches])
        
        # 过滤合理的价格范围（30-100元/小时）
        prices = [p for p in prices if 30 <= p <= 100]
        
        return list(set(prices))  # 去重
    
    def crawl_58com(self, pages=3):
        """爬取58同城"""
        print("="*60)
        print("正在爬取 58同城...")
        print("="*60)
        
        for page in range(1, pages + 1):
            print(f"\n第 {page} 页:")
            
            if page == 1:
                url = "bj.58.com/zhongdiangong/"
            else:
                url = f"bj.58.com/zhongdiangong/pn{page}/"
            
            text = self.fetch_jina(url)
            if not text:
                continue
            
            prices = self.extract_prices(text, "58同城")
            print(f"  找到 {len(prices)} 个价格: {prices}")
            
            for price in prices:
                self.results.append({
                    'platform': '58同城',
                    'page': page,
                    'price': price,
                    'unit': '元/小时',
                    'crawl_time': datetime.now().isoformat()
                })
            
            time.sleep(2)
    
    def crawl_58com_chaoyang(self):
        """爬取58同城朝阳区"""
        print("\n" + "="*60)
        print("正在爬取 58同城-朝阳区...")
        print("="*60)
        
        url = "bj.58.com/chaoyang/zhongdiangong/"
        text = self.fetch_jina(url)
        
        if text:
            prices = self.extract_prices(text, "58同城-朝阳")
            print(f"  找到 {len(prices)} 个价格: {prices}")
            
            for price in prices:
                self.results.append({
                    'platform': '58同城-朝阳区',
                    'page': 1,
                    'price': price,
                    'unit': '元/小时',
                    'crawl_time': datetime.now().isoformat()
                })
    
    def crawl_ganji(self, pages=2):
        """爬取赶集网"""
        print("\n" + "="*60)
        print("正在爬取赶集网...")
        print("="*60)
        
        for page in range(1, pages + 1):
            print(f"\n第 {page} 页:")
            
            if page == 1:
                url = "bj.ganji.com/zhongdiangong/"
            else:
                url = f"bj.ganji.com/zhongdiangong/o{page}/"
            
            text = self.fetch_jina(url)
            if not text:
                continue
            
            prices = self.extract_prices(text, "赶集网")
            print(f"  找到 {len(prices)} 个价格: {prices}")
            
            for price in prices:
                self.results.append({
                    'platform': '赶集网',
                    'page': page,
                    'price': price,
                    'unit': '元/小时',
                    'crawl_time': datetime.now().isoformat()
                })
            
            time.sleep(2)
    
    def crawl_meituan(self):
        """爬取美团家政"""
        print("\n" + "="*60)
        print("正在爬取美团...")
        print("="*60)
        
        # 美团家政服务页面
        urls = [
            "bj.meituan.com/s/%E9%92%9F%E7%82%B9%E5%B7%A5/",
            "bj.meituan.com/s/%E5%AE%B6%E6%94%BF/",
        ]
        
        for url in urls:
            print(f"\n尝试: {url}")
            text = self.fetch_jina(url)
            
            if text:
                prices = self.extract_prices(text, "美团")
                print(f"  找到 {len(prices)} 个价格: {prices}")
                
                for price in prices:
                    self.results.append({
                        'platform': '美团',
                        'page': 1,
                        'price': price,
                        'unit': '元/小时',
                        'crawl_time': datetime.now().isoformat()
                    })
            
            time.sleep(2)
    
    def crawl_dianping(self):
        """爬取大众点评"""
        print("\n" + "="*60)
        print("正在爬取大众点评...")
        print("="*60)
        
        # 大众点评家政服务
        urls = [
            "www.dianping.com/beijing/ch10/g165",
            "www.dianping.com/beijing/ch10/g34235",
        ]
        
        for url in urls:
            print(f"\n尝试: {url}")
            text = self.fetch_jina(url)
            
            if text:
                prices = self.extract_prices(text, "大众点评")
                print(f"  找到 {len(prices)} 个价格: {prices}")
                
                for price in prices:
                    self.results.append({
                        'platform': '大众点评',
                        'page': 1,
                        'price': price,
                        'unit': '元/小时',
                        'crawl_time': datetime.now().isoformat()
                    })
            
            time.sleep(2)
    
    def analyze(self):
        """分析结果"""
        print("\n" + "="*60)
        print("📊 数据分析")
        print("="*60)
        
        if not self.results:
            print("❌ 没有获取到数据")
            return None
        
        import pandas as pd
        df = pd.DataFrame(self.results)
        
        print(f"\n总计: {len(self.results)} 条数据")
        
        print(f"\n按平台统计:")
        platform_stats = df.groupby('platform')['price'].agg(['count', 'mean', 'min', 'max'])
        print(platform_stats)
        
        print(f"\n整体统计:")
        print(f"  最低: {df['price'].min()} 元/小时")
        print(f"  最高: {df['price'].max()} 元/小时")
        print(f"  平均: {df['price'].mean():.1f} 元/小时")
        print(f"  中位: {df['price'].median():.1f} 元/小时")
        
        # 你的情况分析
        print("\n" + "="*60)
        print("🎯 你的情况分析")
        print("="*60)
        user_price = 40
        market_avg = df['price'].mean()
        print(f"你的价格: {user_price} 元/小时")
        print(f"市场平均: {market_avg:.1f} 元/小时")
        print(f"差距: {market_avg - user_price:.1f} 元/小时 ({((market_avg - user_price)/user_price*100):.1f}%)")
        
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
            import pandas as pd
            csv_file = f'data/prices_{self.timestamp}.csv'
            df = pd.DataFrame(self.results)
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"✅ CSV 保存: {csv_file}")
            
            # 汇总
            summary_file = 'data/latest_summary.csv'
            summary = df.groupby('platform')['price'].agg(['count', 'mean', 'min', 'max']).reset_index()
            summary.columns = ['平台', '样本数', '平均价格', '最低价格', '最高价格']
            summary.to_csv(summary_file, index=False, encoding='utf-8-sig')
            print(f"✅ 汇总保存: {summary_file}")
            
            return df
        
        return None
    
    def run(self):
        """运行所有爬虫"""
        print("🚀 开始爬取北京钟点工价格数据...\n")
        
        self.crawl_58com(pages=3)
        self.crawl_58com_chaoyang()
        self.crawl_ganji(pages=2)
        self.crawl_meituan()
        self.crawl_dianping()
        
        df = self.analyze()
        self.save()
        
        print("\n✅ 完成!")
        return df

if __name__ == '__main__':
    crawler = PriceCrawler()
    crawler.run()
