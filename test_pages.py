#!/usr/bin/env python
import requests
import re

try:
    response = requests.get('http://127.0.0.1:5000/Bagues')
    if response.status_code == 200:
        html = response.text
        # Find img tags
        img_tags = re.findall(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*>', html)
        print(f'Found {len(img_tags)} image tags')
        for i, src in enumerate(img_tags[:10]):
            print(f'  {i}: {src}')
        if len(img_tags) > 10:
            print(f'  ... and {len(img_tags) - 10} more')
        
        # Check for any error messages
        if 'error' in html.lower() or 'exception' in html.lower():
            print('\nERROR FOUND IN HTML:')
            print(html[-500:])
    else:
        print(f'Error: {response.status_code}')
        print(response.text[:500])
except Exception as e:
    print(f'Exception: {e}')
