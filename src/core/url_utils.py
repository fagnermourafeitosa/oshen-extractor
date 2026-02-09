from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import Dict, Set

# Tracking parameters to remove from URLs
INSTAGRAM_TRACKING_PARAMS: Set[str] = {
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
    'igsh', 'igshid', 'ig_rid', 'ig_web_copy_link'
}

TIKTOK_TRACKING_PARAMS: Set[str] = {
    'is_from_webapp', 'sender_device', 'web_id', 'is_copy_url',
    'utm_source', 'utm_medium', 'utm_campaign'
}

def sanitize_url(url: str) -> str:
    """
    Remove unnecessary tracking and query parameters from social media URLs.
    
    Args:
        url: The original URL with potential tracking parameters
        
    Returns:
        Cleaned URL with only essential parameters
    """
    parsed = urlparse(url)
    
    # If no query string, return as-is
    if not parsed.query:
        return url
    
    query_params = parse_qs(parsed.query)
    
    # Determine which tracking params to remove based on domain
    tracking_params = set()
    if 'instagram.com' in parsed.netloc:
        tracking_params = INSTAGRAM_TRACKING_PARAMS
    elif 'tiktok.com' in parsed.netloc:
        tracking_params = TIKTOK_TRACKING_PARAMS
    
    # Filter out tracking parameters
    cleaned_params = {
        key: value 
        for key, value in query_params.items() 
        if key not in tracking_params
    }
    
    # Rebuild query string
    new_query = urlencode(cleaned_params, doseq=True)
    
    # Return cleaned URL
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
