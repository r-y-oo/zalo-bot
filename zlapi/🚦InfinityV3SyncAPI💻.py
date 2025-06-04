"""
📑InfinityV3SyncClient - Turbo-powered Sync HTTP Client with Cache, Proxy, and Stats🎮

💻Created by: Kai💢
🚦Version: 3.0🚀

"""

import requests
import random
import time
import threading
import statistics
import logging
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import requests
import random
import time
import threading
import statistics
import logging
from collections import deque
from concurrent.futures import ThreadPoolExecutor

class InfinityV3SyncClient:
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
        self.default_headers = {"User-Agent": "InfinityV3Client/0.0"}
        self.stats = {
            "total_requests": 0,
            "failed_requests": 0,
            "cache_hits": 0,
            "response_times": deque(maxlen=1000)
        }
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

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

# Tạo instance có sẵn
infinity_v3_sync_client = InfinityV3SyncClient()