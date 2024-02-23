from setuptools import setup, find_packages

setup(
    name='google-maps-scraper-api',
    version='0.1.0',
    packages=find_packages(),
    author='Oxylabs',
    author_email='marketing@oxylabs.io',
    description="Google Maps Scraper for collecting data from various Google Maps listings, including business profiles.",
    long_description="""# Google Maps Scraper
[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

Google Maps Scraper enables effortless public data extraction with
geographic references from Google Maps and Google Places. This short
guide will show you the process of scraping Google Maps using Oxylabs'
Scraper API.

## How it works

You can retrieve Google Maps data by providing the URL to our service.
Our API will return the results in JSON format.

### Python code example

The below code examples demonstrate how you can get Google Maps results.
First, you need to send the instructions to our service using the
[<u>Push-Pull</u>](https://developers.oxylabs.io/scraper-apis/getting-started/integration-methods/push-pull)
method:

```python
import requests
from pprint import pprint

# Structure payload.
payload = {
    'source': 'google',
    'url': 'https://www.google.com/maps/search/restaurants/@40.7660158,-73.9833944,14z/data=!4m5!2m4!5m2!1e0!4e9!6e5?entry=ttu',
    'geo_location': 'New York,New York,United States',
    'render': 'html'
}

# Get response.
response = requests.request(
    'POST',
    'https://data.oxylabs.io/v1/queries',
    auth=('USERNAME', 'PASSWORD'),
    json=payload
)

# This will return a response with job status and results url.
pprint(response.json())

```

Once the job is done, you can retrieve the results by making another
request and including the **job ID** from the previous response, for
instance:

```python
import requests

# Get response.
response = requests.request(
    'GET',
    'http://data.oxylabs.io/v1/queries/{job_id}/results',
    auth=('USERNAME', 'PASSWORD')
)

# This will return the JSON response with results.
print(response.json())

```

### Output Example

The above code snippet will retrieve the results in JSON format:

```json
{
    "results": [
        {
            "content": "<!doctype html>\n<html lang=\"en\">\n<head>...</script></body>\n</html>\n",
            "created_at": "2023-07-25 10:01:01",
            "job_id": "7089545068712824833",
            "page": 1,
            "status_code": 200,
            "updated_at": "2023-07-25 10:01:20",
            "url": "https://www.google.com/maps/search/restaurants/@40.7660158,-73.9833944,14z/data=!4m5!2m4!5m2!1e0!4e9!6e5?entry=ttu"
        }
    ]
}
```

From local landmarks to various businesses, with Oxylabs’ Google Maps
Scraper you’ll easily access the public data you need. If you have any
questions or need assistance, don’t hesitate to contact our 24/7 support
team via live chat or [<u>email</u>](mailto:support@oxylabs.io).

""",
    long_description_content_type='text/markdown',
    url='https://oxylabs.io/products/scraper-api/serp/google/maps',
    project_urls={
        'Documentation': 'https://developers.oxylabs.io/scraper-apis/serp-scraper-api/google?_gl=1*1ogqnhx*_gcl_aw*R0NMLjE3MDg1MTU0ODYuQ2p3S0NBaUEyOWF1QmhCeEVpd0FuS2NTcWtRSWlmdl9Ud19pcWxkM3hSTVNNa1E4SHlCM3p0TDFzdnA5aTE1N0lYckNGQWVtRUdiY29ob0NhUVlRQXZEX0J3RQ..*_gcl_au*MTc2MDgxNTAwNC4xNzA1OTI3MzM0',
        'Source': 'https://github.com/oxylabs/google-maps-scraper',
        'Bug Reports': 'https://github.com/oxylabs/google-maps-scraper/tree/main/issues',
    },
    keywords='google-maps-scraper,	google-maps-api,	google-maps-scraping,	google-maps-scrape',
    license='MIT',

    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
)









