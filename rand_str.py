import string
import random

# n in a int, number of char for the random string
def rand_str(n=20):
  # returns a n size list
  result = random.choices(string.ascii_lowercase + string.digits + string.ascii_letters, k=n)

  return "".join(result)
