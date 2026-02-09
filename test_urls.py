#!/usr/bin/env python3
"""Test script to diagnose Instagram and TikTok download issues"""

import sys
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.social_networks.use_cases.download_media import DownloadMediaUseCase

def clean_url(url: str) -> str:
    """Remove unnecessary query parameters from URLs"""
    parsed = urlparse(url)
    
    if 'instagram.com' in parsed.netloc:
        # Keep only essential Instagram params if any
        query_params = parse_qs(parsed.query)
        essential_params = {}
        new_query = urlencode(essential_params, doseq=True)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    
    elif 'tiktok.com' in parsed.netloc:
        # Keep only essential TikTok params if any
        query_params = parse_qs(parsed.query)
        essential_params = {}
        new_query = urlencode(essential_params, doseq=True)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    
    return url

def test_download(url: str, name: str):
    """Test downloading a URL"""
    print(f"\n{'='*80}")
    print(f"Testing: {name}")
    print(f"Original URL: {url}")
    
    cleaned = clean_url(url)
    print(f"Cleaned URL: {cleaned}")
    
    use_case = DownloadMediaUseCase()
    
    try:
        print(f"\nAttempting download with original URL...")
        result = use_case.execute(url, name)
        print(f"✅ SUCCESS: Downloaded to {result}")
        return True
    except Exception as e:
        print(f"❌ FAILED with original URL: {e}")
        
        if cleaned != url:
            try:
                print(f"\nAttempting download with cleaned URL...")
                result = use_case.execute(cleaned, name)
                print(f"✅ SUCCESS: Downloaded to {result}")
                return True
            except Exception as e2:
                print(f"❌ FAILED with cleaned URL: {e2}")
        
        return False

if __name__ == "__main__":
    instagram_url = "https://www.instagram.com/reel/DUgcMZ4jl8w/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ=="
    tiktok_url = "https://www.tiktok.com/@promoshop.on/video/7579286134551874837?is_from_webapp=1&sender_device=pc"
    
    results = []
    results.append(("Instagram", test_download(instagram_url, "instagram_test")))
    results.append(("TikTok", test_download(tiktok_url, "tiktok_test")))
    
    print(f"\n{'='*80}")
    print("SUMMARY:")
    for platform, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {platform}: {status}")
