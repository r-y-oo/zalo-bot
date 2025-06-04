"""
📁APIkailimitedMAX - Turbo-powered Sync & Async HTTP Client with Cache, Proxy, Stats, File Download, Auto-Unblock & Ultra-Spam🎮

💻Created by: Kai💢
🚦Version: 5.0 MAXIMUM OVERDRIVE🚀
"""

import requests
import random
import time
import threading
import statistics
import logging
import os
import asyncio
import aiohttp
from collections import deque
from concurrent.futures import ThreadPoolExecutor

class APIkailimitedMAX:
    def __init__(self,
                 max_workers=200,
                 retry_attempts=5,
                 timeout=5,
                 cache_ttl=60,
                 turbo_mode=True,
                 debug=False,
                 response_hook=None,
                 error_hook=None):
        self.session = requests.Session()
        self.retry_attempts = retry_attempts
        self.timeout = timeout
        self.cache_ttl = cache_ttl
        self.turbo_mode = turbo_mode
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.cache = {}
        self.lock = threading.Lock()
        self.response_hook = response_hook
        self.error_hook = error_hook

        self.proxy_list = [
            "http://proxy1.com", "http://proxy2.com", "http://proxy3.com"
        ]
        self.dead_proxies = set()
        self.headers_list = [
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
            {"User-Agent": "Mozilla/5.0 (Linux; Android 10)"},
        ]
        self.default_headers = {"User-Agent": "APIkailimitedMAX/5.0"}
        self.stats = {
            "total_requests": 0,
            "failed_requests": 0,
            "cache_hits": 0,
            "response_times": deque(maxlen=1000)
        }
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        self._start_cache_cleaner()

    def _get_proxy(self):
        choices = [p for p in self.proxy_list if p not in self.dead_proxies]
        return random.choice(choices) if choices else None

    def _is_cached(self, url):
        with self.lock:
            entry = self.cache.get(url)
            if entry:
                timestamp, data = entry
                if time.time() - timestamp < self.cache_ttl:
                    self.stats["cache_hits"] += 1
                    return data
                else:
                    del self.cache[url]
            return None

    def invalidate_cache(self, url=None):
        with self.lock:
            if url:
                self.cache.pop(url, None)
            else:
                self.cache.clear()

    def _start_cache_cleaner(self, interval=60):
        def cleaner():
            while True:
                with self.lock:
                    now = time.time()
                    expired = [k for k, (t, _) in self.cache.items() if now - t >= self.cache_ttl]
                    for k in expired:
                        del self.cache[k]
                time.sleep(interval)
        t = threading.Thread(target=cleaner, daemon=True)
        t.start()

    def fetch(self, url, params=None, headers=None, use_cache=True):
        if use_cache:
            cached = self._is_cached(url)
            if cached:
                return cached

        for attempt in range(self.retry_attempts):
            self.stats["total_requests"] += 1
            try:
                proxy = self._get_proxy() if self.turbo_mode else None
                req_headers = headers or random.choice(self.headers_list) or self.default_headers
                start = time.time()
                response = self.session.get(
                    url,
                    params=params,
                    headers=req_headers,
                    proxies={"http": proxy, "https": proxy} if proxy else None,
                    timeout=self.timeout
                )
                elapsed = time.time() - start
                self.stats["response_times"].append(elapsed)

                if response.status_code == 200:
                    data = response.json()
                    with self.lock:
                        self.cache[url] = (time.time(), data)
                    if self.response_hook:
                        self.response_hook(data, url)
                    return data
                else:
                    logging.warning(f"[{response.status_code}] {url}")
            except Exception as e:
                self.stats["failed_requests"] += 1
                if proxy:
                    self.dead_proxies.add(proxy)
                if self.error_hook:
                    self.error_hook(e, url)
                time.sleep(random.uniform(0.1, 0.3))
        logging.error(f"[FAIL] GET {url} failed after {self.retry_attempts} attempts.")
        return None

    def post(self, url, data=None, headers=None):
        for attempt in range(self.retry_attempts):
            self.stats["total_requests"] += 1
            try:
                proxy = self._get_proxy() if self.turbo_mode else None
                req_headers = headers or random.choice(self.headers_list) or self.default_headers
                response = self.session.post(
                    url,
                    json=data,
                    headers=req_headers,
                    proxies={"http": proxy, "https": proxy} if proxy else None,
                    timeout=self.timeout
                )
                if response.status_code == 200:
                    result = response.json()
                    if self.response_hook:
                        self.response_hook(result, url)
                    return result
                else:
                    logging.warning(f"[{response.status_code}] {url}")
            except Exception as e:
                self.stats["failed_requests"] += 1
                if proxy:
                    self.dead_proxies.add(proxy)
                if self.error_hook:
                    self.error_hook(e, url)
                time.sleep(random.uniform(0.1, 0.3))
        logging.error(f"[FAIL] POST {url} failed after {self.retry_attempts} attempts.")
        return None

    def batch_fetch(self, urls, use_cache=True):
        futures = [
            self.executor.submit(self.fetch, url, None, None, use_cache)
            for url in urls
        ]
        return [f.result() for f in futures]

    def prefetch(self, urls):
        results = self.batch_fetch(urls, use_cache=False)
        for url, response in zip(urls, results):
            if response:
                with self.lock:
                    self.cache[url] = (time.time(), response)

    def stats_report(self):
        try:
            avg_time = statistics.mean(self.stats["response_times"])
        except statistics.StatisticsError:
            avg_time = 0.0
        return {
            "Total Requests": self.stats["total_requests"],
            "Failures": self.stats["failed_requests"],
            "Cache Hits": self.stats["cache_hits"],
            "Avg Response Time (s)": round(avg_time, 4),
            "Active Proxies": len(self.proxy_list) - len(self.dead_proxies)
        }

    def download_file(self, url, path):
        try:
            proxy = self._get_proxy() if self.turbo_mode else None
            headers = random.choice(self.headers_list)
            response = self.session.get(
                url,
                headers=headers,
                proxies={"http": proxy, "https": proxy} if proxy else None,
                timeout=self.timeout,
                stream=True
            )
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logging.info(f"Downloaded: {path}")
                return True
        except Exception as e:
            logging.error(f"Download failed: {e}")
        return False

    def auto_unblock(self, group_id):
        """
        Gửi tương tác giả để tránh bị chặn trong nhóm (mõm bot).
        """
        fake_interactions = [
            {"type": "like"}, {"type": "emoji"}, {"type": "seen"},
            {"type": "typing"}, {"type": "ping"}, {"type": "react"}
        ]
        for interaction in fake_interactions:
            try:
                self.post(f"https://chat.zalo.me/api/group/{group_id}/interaction", data=interaction)
                time.sleep(0.1)
            except Exception as e:
                logging.warning(f"Auto unblock failed: {e}")

    def ultra_spam(self, group_id, message, count=10, delay=0.1):
        """
        Gửi nhiều tin nhắn cực nhanh vào nhóm Zalo.
        Nếu bị mõm, chờ 60s rồi thử tiếp.
        """
        success = 0
        i = 0
        while i < count:
            payload = {"message": f"{message} [{i+1}/{count}]"}
            res = self.post(f"https://chat.zalo.me/api/group/{group_id}/message", data=payload)
            if res:
                success += 1
                i += 1
                time.sleep(delay)
            else:
                logging.warning(f"Spam {i+1} failed. Bot có thể đang bị mõm. Chờ 60s...")
                self.auto_unblock(group_id)
                time.sleep(60)
        logging.info(f"Ultra spam done: {success}/{count} messages sent.")

class APIkailimitedMAXAsync:
    def __init__(self, timeout=5, retry_attempts=5):
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.session = aiohttp.ClientSession()

    async def fetch(self, url, params=None):
        for _ in range(self.retry_attempts):
            try:
                async with self.session.get(url, params=params, timeout=self.timeout) as resp:
                    if resp.status == 200:
                        return await resp.json()
            except Exception:
                await asyncio.sleep(0.2)
        return None

    async def post(self, url, data=None):
        for _ in range(self.retry_attempts):
            try:
                async with self.session.post(url, json=data, timeout=self.timeout) as resp:
                    if resp.status == 200:
                        return await resp.json()
            except Exception:
                await asyncio.sleep(0.2)
        return None

    async def close(self):
        await self.session.close()

apikailimited_client = APIkailimitedMAX()
async_client = APIkailimitedMAXAsync()