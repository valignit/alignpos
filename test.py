import http.client

conn = http.client.HTTPSConnection("skhic.erpnext.com")
payload = ''
headers = {
  'Authorization': 'token e3027624ee468a2:65786fb05aebfac'
}
conn.request("GET", "/api/resource/Item", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))