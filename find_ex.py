def find_extension(img_url):
  if img_url.endswith("/"):
    img_url = img_url[:len(img_url)-1]

  rev_link = img_url[::-1]
  rev_link = rev_link.split(".")

  return rev_link[0][::-1]
