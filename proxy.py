from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._proxy_request('GET')

    def do_POST(self):
        self._proxy_request('POST')

    def _proxy_request(self, method):
        try:
            
            parsed_url = urlparse(self.path)

            full_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment
            ))

            # Get the body if it's a POST request
            if method == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                response = requests.post(full_url, data=post_data, headers=self.headers)
            else:
                print(f"Get request: {full_url}")
                response = requests.get(full_url, headers=self.headers)
            
            # Send response status code
            self.send_response(response.status_code)
            self.send_header("Content-type", response.headers.get('Content-Type', 'text/html'))
            self.send_header("Set-Cookie", response.headers.get('Set-Cookie', 'text/html'))
            self.end_headers()
            
            # Write the response content
            self.wfile.write(response.content)
        except Exception as e:
            self.send_error(500, str(e))

def run(server_class=HTTPServer, handler_class=ProxyHTTPRequestHandler, port=9999):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
