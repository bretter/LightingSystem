import SimpleHTTPServer, SocketServer, os

PORT = 8000

os.chdir('../LightingSystem/webServer/')

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print 'Serving HTTP at port', PORT

httpd.serve_forever()
