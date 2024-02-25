import os

from mediqbox.abc.async2sync import Async2Sync
from mediqbox.download.download import (
  Download,
  DownloadConfig,
  DownloadInputData
)

def test_download():
  target_dir = os.path.join(os.path.dirname(__file__), 'test_results')

  # Remove files in target_dir
  for item in os.listdir(target_dir):
    fullpath = os.path.join(target_dir, item)
    if os.path.isfile(fullpath):
      os.unlink(fullpath)

  input_data = DownloadInputData(urls=[
    "https://snqueue-public.s3.amazonaws.com/en.txt",
    "https://snqueue-public.s3.amazonaws.com/en.pdf"
  ])

  downloader = Async2Sync(Download(DownloadConfig(
    target_dir=target_dir
  )))

  result = downloader.process(input_data)
  print(result)

  assert len(result) == 2 and os.path.isfile(result[0]) and os.path.isfile(result[1])

if __name__ == '__main__':
  test_download()