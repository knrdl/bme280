import bme280
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlsplit


class Server(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def send(self, content: str, code: int, mime: str):
        content = content.encode('utf8')
        self.send_response(code)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        try:
            url = urlsplit(self.path.strip() or '/')
            if url.path == '/metrics':
                temperature, humidity, pressure = bme280.read_measurements()
                output = ''
                output += f'HELP bme280_temperature Temperature in celsius' + '\n'
                output += f'TYPE bme280_temperature gauge' + '\n'
                output += f'bme280_temperature {temperature}' + '\n'
                output += f'HELP bme280_humidity Humidity in percent' + '\n'
                output += f'TYPE bme280_humidity gauge' + '\n'
                output += f'bme280_humidity {humidity}' + '\n'
                output += f'HELP bme280_pressure Pressure in hectopascals' + '\n'
                output += f'TYPE bme280_pressure gauge' + '\n'
                output += f'bme280_pressure {pressure}' + '\n'
                return self.send(output, code=200, mime='text/plain; version=0.0.4')
            elif url.path == '/':
                temperature, humidity, pressure = bme280.read_measurements()
                data = {'temperature': temperature, 'humidity': humidity, 'pressure': pressure}
                return self.send(json.dumps(data) + '\n', code=200, mime='application/json')
            return self.send('404 not found', code=404, mime='text/plain')
        except Exception as e:
            traceback.print_exc()
            return self.send(str(e), code=500, mime='text/plain')


HTTPServer(('', 8080), Server).serve_forever()
