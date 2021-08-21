import urllib.request

req = urllib.request.Request("https://yahoo.co.jp")

res = urllib.request.urlopen(req)
if res.getcode() != 200:
    print("error")

body = res.read()

res.close()

print(body) # bytes
print(type(body))