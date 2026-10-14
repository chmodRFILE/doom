# Opera Browser Tarball

This directory contains the Opera browser tarball for spider generation.

## Download

Opera can be downloaded from:
https://get.geo.opera.com/pub/opera/desktop/

## Contents

- opera.tar.xz: Main Opera browser tarball
- opera: Opera executable

## Usage

To extract and use:
```bash
# Extract the tarball
tar -xJf opera.tar.xz

# Use with Selenium (if needed)
from selenium import webdriver
driver = webdriver.Opera(executable_path='opera/opera')
```

## Features for Spiders

- Chromium-based engine
- Built-in ad blocker
- Good JavaScript execution
- Modern web standards compliance
- Lightweight compared to Chrome
- Excellent compatibility with modern web applications

## Integration Tips

For spider generation, consider:
1. Leveraging the built-in ad blocker for cleaner scraping
2. Using the Chromium engine for better JavaScript support
3. Configuring appropriate user agents
4. Managing browser profiles for session persistence