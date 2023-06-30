import requests

# Set your ProxyCrawl token
proxy_crawl_token = 'W6iEsEvjfVB8k4EOvFr2gg'

# Specify the URL you want to scrape
url = 'https://www.kroger.com'

# Construct the API request URL with the ProxyCrawl token and URL
api_url = f'https://api.proxycrawl.com/?token={proxy_crawl_token}&url={url}'

session = requests.Session()

login_url = 'https://www.kroger.com/signin?redirectUrl=/'
response = session.get(login_url, timeout=10)

payload = {
        "email": "crstt.code@gmail.com",
        "password": "123Stella",
        "rememberMe": True
    }

login_action_url = 'https://www.kroger.com/auth/api/sign-in'
response = session.post(login_action_url, data=payload)

if response.status_code == 200:
    if 'Login successful' in response.text:
        print('Login successful')
    else:
        print('Login failed')
else:
    print('Error occurred during login')

# Send the GET request to the ProxyCrawl API
#sresponse = requests.get(api_url)

# Access the HTML content of the response
html_content = response.text

# Print the HTML content
print(html_content)
