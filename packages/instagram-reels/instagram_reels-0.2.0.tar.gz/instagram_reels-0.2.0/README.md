<h1 align="center">
  Reels Downloader
</h1>
<p align="center">
    <em><b>Помогает получить прямую ссылку на reels в разных разрешениях</b></em>
</p>

## Установка

Установить новейшую версию можно командой:

```shell
pip install downloader-for-reels
```

## Пример работы

Скачивание reels:

```python
import asyncio
import requests
from reels_downloader.main.Reels import Reels

SESSION_ID = "your_session"


async def download_reels(clip_name: str, reel_id: str):
    my_reels = Reels(SESSION_ID)
    info = await my_reels.get(reel_id)
    with open(clip_name, "wb+") as out_file:
        out_file.write((requests.get(info.videos[0].url)).content)


asyncio.run(download_reels("example.mp4", "1234"))
```
