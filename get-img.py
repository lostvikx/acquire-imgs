from bs4 import BeautifulSoup
import urllib3
import os
import re
from find_ex import find_extension
import urllib.request
from string import punctuation

print("Welcome HTML Image Parser")

# Current working dir (no "/" at the end)
path = os.getcwd()

url = input("Enter URL: ")

# Add https:// before the input url
if not url.startswith("http://") and not url.startswith("https://"):
  url = "https://" + url

http = urllib3.PoolManager()

res = http.request(
  "GET",
  url,
  preload_content=False
)

html = b""

for chunk in res.stream(1024):
  html += chunk

res.release_conn()

soup = BeautifulSoup(html, "html.parser")

# List of img tags
img_tags = soup.find_all("img")

img_dict = {}

image_count = 1

for tag in img_tags:
  # Get attr
  img_link = tag.get("src").strip()
  img_title = tag.get("alt")

  # If no or blank alt attr then give arbitrary filename
  if img_title is None or img_title == "":
    img_title = "img-" + str(image_count)
    image_count += 1
  else:
    img_title = img_title.strip()
    img_title = img_title.translate(img_title.maketrans("", "", punctuation))
    img_title = re.sub(r"\s", "_", img_title)

  # Pretty good stuff
  if not re.search(r"^http[s]?://", img_link):
    if re.search(r"^/", img_link):
      img_dict[img_title] = url + img_link
    else:
      img_dict[img_title] = url + "/" + img_link
  else:
    img_dict[img_title] = img_link

print(url)
print(img_dict)

download_complete = 0

for (title, link) in list(img_dict.items()):
  file_ext = find_extension(link).strip()

  res_img = urllib.request.urlopen(link)

  try:
    os.remove(f"{path}/imgs/{title}.{file_ext}")
  except:
    pass

  try:
    file_handle = open(f"./imgs/{title}.{file_ext}", "wb")
  except:
    print("img not saved")
    file_handle.close()
    continue

  i_size = 0

  while True:
    info = res_img.read(1024)
    i_size += len(info)
    if len(info) < 1: break

    if file_handle.writable(): file_handle.write(info)
    else: 
      print("file not writable")
      file_handle.close()

  print(f"download file complete size: {i_size}")
  download_complete += 1
  file_handle.close()

print("Execution Complete")
print(f"{download_complete} files were downloaded")
