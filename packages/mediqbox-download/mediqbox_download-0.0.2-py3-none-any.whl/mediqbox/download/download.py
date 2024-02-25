import logging
import os

import aiofiles
import aiohttp
import asyncio

from collections.abc import Iterable
from pydantic import field_validator, Field
from typing import Optional
from urllib.parse import unquote

from mediqbox.abc.abc_component import (
  AbstractComponent,
  ComponentConfig,
  InputData
)

class DownloadConfig(ComponentConfig):
  target_dir: str
  max_workers: int = Field(ge=1, default=5)

  @field_validator('target_dir')
  @classmethod
  def is_dir(cls, v: str):
    if not os.path.isdir(v):
      raise ValueError(f"{v} is not a valid directory")
    return v

class DownloadInputData(InputData):
  urls: Iterable[str]

class Download(AbstractComponent):

  async def _download_single(
      self,
      semaphore: asyncio.Semaphore,
      session: aiohttp.ClientSession,
      url: str,
  ) -> Optional[str]:
    target_dir = self.config.target_dir

    async with semaphore:
      async with session.get(url) as r:
        if not r.status == 200:
          logging.error(f"Error when downloading {url}")
          logging.error(f"  status: {r.status}, reason: {r.reason}")
          return None
    
        header = r.headers.get("content-disposition")
        if header:
          filename = header.split("filename=")[1]
          if ((filename.startswith('"') and   filename.endswith('"')) or
            (filename.startswith("'") and filename.endswith("'"))):
            filename = filename[1:-1]
        else:
          filename = unquote(url.split('?')[0].split('/')[-1])
        filepath = os.path.join(target_dir, filename)

        async with aiofiles.open(filepath, mode="wb") as f:
          await f.write(await r.read())
          return filepath
    
  async def process(self, input_data: DownloadInputData) -> list[str]:
    semaphore = asyncio.Semaphore(self.config.max_workers)
    async with aiohttp.ClientSession() as session:
      tasks = map(
        lambda url: self._download_single(
          semaphore,
          session,
          url
        ),
        input_data.urls
      )
      return await asyncio.gather(*tasks)