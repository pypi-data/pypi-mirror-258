# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['instagram_reels',
 'instagram_reels.api',
 'instagram_reels.api.private',
 'instagram_reels.api.private.client',
 'instagram_reels.api.private.parser',
 'instagram_reels.api.private.service',
 'instagram_reels.api.public',
 'instagram_reels.api.public.client',
 'instagram_reels.api.public.model',
 'instagram_reels.api.public.parser',
 'instagram_reels.api.public.service',
 'instagram_reels.api.public.util',
 'instagram_reels.common',
 'instagram_reels.common.model',
 'instagram_reels.main',
 'instagram_reels.reels']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp==3.8.3',
 'aiosignal==1.3.1',
 'async-timeout==4.0.2',
 'attrs==22.2.0',
 'beautifulsoup4==4.11.2',
 'charset-normalizer==2.1.1',
 'frozenlist==1.3.3',
 'idna==3.4',
 'instagram-auth==0.1.1',
 'multidict==6.0.4',
 'soupsieve==2.3.2.post1',
 'yarl==1.8.2']

setup_kwargs = {
    'name': 'instagram-reels',
    'version': '0.2.0',
    'description': 'Instagram Reels Downloader',
    'long_description': '<h1 align="center">\n  Reels Downloader\n</h1>\n<p align="center">\n    <em><b>Помогает получить прямую ссылку на reels в разных разрешениях</b></em>\n</p>\n\n## Установка\n\nУстановить новейшую версию можно командой:\n\n```shell\npip install downloader-for-reels\n```\n\n## Пример работы\n\nСкачивание reels:\n\n```python\nimport asyncio\nimport requests\nfrom reels_downloader.main.Reels import Reels\n\nSESSION_ID = "your_session"\n\n\nasync def download_reels(clip_name: str, reel_id: str):\n    my_reels = Reels(SESSION_ID)\n    info = await my_reels.get(reel_id)\n    with open(clip_name, "wb+") as out_file:\n        out_file.write((requests.get(info.videos[0].url)).content)\n\n\nasyncio.run(download_reels("example.mp4", "1234"))\n```\n',
    'author': 'Николай Витальевич Никоноров',
    'author_email': 'nnv@bitt.moe',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/bitt_moe/instagram/reels_downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
