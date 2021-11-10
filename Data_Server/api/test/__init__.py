#api.test
print("Importing test plugin...")

import general
import api
import api.common as common

def url_hook(path):
    if general.isEndpoint(path,"/test"):
        resp = {"data": None, "func": give_test_response}
        return resp
    else:
        return None

# api.urlHooks += [url_hook]

async def give_test_response(data):
    print("api.test.give_test_response2 triggered.")
    response = {
        "Code": 200,
        "Headers": general.XML_HEADERS,
        "Body": 
            b'<?xml version="1.0" encoding="utf-8"?>' +
            b'<rss>' +
            b'<channel>' +
            b'<first>Hello World!</first>' +
            b'<second>The server is operational.</second>' +
            b'</channel>' +
            b'</rss>'
        }
    
    return response

common.set_up_url_hooks()

print("Test plugin imported successfully!")