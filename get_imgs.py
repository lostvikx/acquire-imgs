from bs4 import BeautifulSoup
import urllib3
import os
import re
from find_ex import find_extension
import urllib.request, urllib.error
from string import punctuation
from rand_str import rand_str

print("Welcome to acquire-imgs")
print("Enter 'q' to quit")

# Current working dir (no "/" at the end)
path = os.getcwd()

while True:

  url = input("Enter URL: ")

  if url == "q": 
    print("Hope you have a lovely day!")
    break

  # Add https:// before the input url
  if not url.startswith("http://") and not url.startswith("https://"):
    url = "https://" + url

  print(f"Retrieving: '{url}'")

  # Using urllib3 library instead of urllib
  http = urllib3.PoolManager()

  # GET request for the entire HTML page
  res = http.request(
    "GET",
    url,
    preload_content=False
  )

  # Storing the page as bytes
  html = b""

  for chunk in res.stream(1024):
    html += chunk

  res.release_conn()

  # Using BS4 to parse the HTML
  soup = BeautifulSoup(html, "html.parser")

  # List of img tags
  img_tags = soup.find_all("img")

  img_dict = {}

  for tag in img_tags:
    # Get src and title attr
    img_link = tag.get("src").strip()
    img_title = tag.get("alt")

    # If blank or no alt attr, then give arbitrary filename
    if img_title is None or img_title == "":
      img_title = rand_str()
    else:
      img_title = img_title.strip()
      img_title = img_title.translate(img_title.maketrans("", "", punctuation))
      img_title = re.sub(r"\s", "_", img_title)

    # Pretty good logic
    if not re.search(r"^http[s]?://", img_link):
      if re.search(r"^/", img_link):
        img_dict[img_title] = url + img_link
      else:
        img_dict[img_title] = url + "/" + img_link
    else:
      img_dict[img_title] = img_link

  # Print the img_dict, { img_title = img_link, ... }
  print(img_dict)

  # n of files downloaded
  download_complete = 0

  for (title, link) in list(img_dict.items()):
    # Find the extension of the img file ["jpg", "png"]
    file_ext = find_extension(link).strip()

    # GET req for the img file, can get a 403 error (Forbidden client)
    try:
      res_img = urllib.request.urlopen(link)
    except urllib.error:
      print("Couldn't fetch img link.")
      print(urllib.error)
      # Continue to the next iteration
      continue

    # This is only for testing purpose.
    # If a file with a similar name exists, remove it.
    try:
      os.remove(f"{path}/imgs/{title}.{file_ext}")
    except:
      # Good stuff
      pass

    # Open file handle to write in bytes
    try:
      file_handle = open(f"./imgs/{title}.{file_ext}", "wb")
    except:
      print("Couldn't open file handle for writing.")
      file_handle.close()
      continue

    # Img size
    i_size = 0

    while True:
      info = res_img.read(1024)
      i_size += len(info)
      if len(info) < 1: break

      # Check if the file handle is writable
      if file_handle.writable(): file_handle.write(info)
      else: 
        print("file not writable")
        file_handle.close()
        break

    print(f"Download Complete: {i_size}bytes")
    download_complete += 1
    file_handle.close()

  print("Execution Complete")
  print(f"{download_complete} files were downloaded!")
