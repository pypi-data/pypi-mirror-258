from setuptools import setup, find_packages

setup(
    name='youtube-video-scraper-api',
    version='0.1.3',
    packages=find_packages(),
    author='Oxylabs',
    author_email='marketing@oxylabs.io',
    description="YouTube Scraper for effortless public YouTube data collection, including video and channel information.",
    long_description="""
<h2 align="center">
   YouTube Scraper
</h2>

[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

With [<u>YouTube
Scraper</u>](https://oxylabs.io/products/scraper-api/web/youtube), you
can easily collect public YouTube data without blocks. Follow this guide
to see how to scrape YouTube using Oxylabs’ [<u>Scraper
API</u>](https://oxylabs.io/products/scraper-api).

## How it works

Simply, send a web request to our API and you’ll retrieve the HTML of
any public YouTube page you wish to scrape.

### Python code example

The below code requests and delivers the HTML content of [<u>this
Oxylabs video</u>](https://www.youtube.com/watch?v=SLSGtgKWzxg) on
YouTube:

```python
import requests
from pprint import pprint

# Structure payload.
payload = {
    'source': 'universal',
    'url': 'https://www.youtube.com/watch?v=SLSGtgKWzxg',
    'render': 'html'
}

# Get a response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('USERNAME', 'PASSWORD'),  # Your credentials go here
    json=payload
)

# Instead of response with job status and results URL, this will return the
# JSON response with results.
pprint(response.json())
```

See Oxylabs
[<u>documentation</u>](https://developers.oxylabs.io/scraper-apis/web-scraper-api)
for more details.

### Output sample

```json
{
    "results": [
        {
            "content":"<!doctype html>\n<html lang=\"en\">\n<head>
            ...
            </script></body>\n</html>\n",
            "created_at": "2023-05-18 12:33:40",
            "updated_at": "2023-05-18 12:33:55",
            "page": 1,
            "url": "https://www.youtube.com/watch?v=SLSGtgKWzxg",
            "job_id": "7064941110115745793",
            "status_code": 200
        }
    ]
}
```

Oxylabs’ YouTube Scraper API will ease your data gathering efforts and
you’ll be sure to gather YouTube data like channel information, video
details, titles, descriptions, playlists, and more. Reach out to us via
[<u>live chat</u>](https://oxylabs.io/) or
[<u>email</u>](mailto:support@oxylabs.io) in case you have any
questions.


""",
    long_description_content_type='text/markdown',
    url='https://oxylabs.io/products/scraper-api/web/youtube',
    project_urls={
        'Documentation': 'https://developers.oxylabs.io/scraper-apis/web-scraper-api?_gl=1*1pp25mi*_gcl_aw*R0NMLjE3MDg1MTU0ODYuQ2p3S0NBaUEyOWF1QmhCeEVpd0FuS2NTcWtRSWlmdl9Ud19pcWxkM3hSTVNNa1E4SHlCM3p0TDFzdnA5aTE1N0lYckNGQWVtRUdiY29ob0NhUVlRQXZEX0J3RQ..*_gcl_au*MTc2MDgxNTAwNC4xNzA1OTI3MzM0',
        'Source': 'https://github.com/oxylabs/youtube-scraper',
        'Bug Reports': 'https://github.com/oxylabs/youtube-scraper/issues',
    },
    keywords='youtube-api,	youtube- scraper,	scrape-youtube, youtube-crawler, scrape-youtube-videos ',
    license='MIT',

    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
)









