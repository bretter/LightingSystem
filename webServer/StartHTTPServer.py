import SimpleHTTPServer
import SocketServer
import os

PORT = 8000

os.chdir('/opt/LightingSystem/webServer/')

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print 'Serving HTTP at port', PORT

try:
	print('serving...')
	httpd.serve_forever()
except KeyboardInterrupt:
	print('Closing socket.')
	httpd.socket.close()
	exit()