Diffbot Knowledge Graph Client
=============

![](https://www.diffbot.com/assets/img/diffbot-logo-darkbg.svg)

Description
-----------

Python client for the Diffbot Knowledge Graph API.

Installation
------------

```sh
pip install diffbot-kg
```

Usage
-----

```python
from diffbot_kg import DiffbotSearchClient, DiffbotEnhanceClient

search_client = DiffbotSearchClient('your_api_key')
enhance_client = DiffbotEnhanceClient('your_api_key')

# Search for entities
search_results = search_client.search({query='type:Organization name:Diffbot'})

# Enhance an entity
enhanced_entity = enhance_client.enhance({query='type:Organization name:Diffbot'})
```

Contributing
------------

Contributions to this project are welcome. - see the CONTRIBUTING.md file for details.

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.
