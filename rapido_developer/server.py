
from http.server import *
import socketserver
import json
import re
import os
from abc import ABC, abstractmethod

import bpy
from pathlib import Path

class BlenderAddonDeveloperHTTPRequestHandler(ABC, BaseHTTPRequestHandler):

    @property
    @abstractmethod
    def router(self): pass

    @property
    @abstractmethod
    def default_route(self): pass

    def do_GET(self):

      for k, v in self.router.items():
        if k.match(self.path):
          result = re.findall(k, self.path)
          getattr(self, v)(*result)
          return
      self.default_route()

    def send_html(self, content):

        out = bytearray(content, 'utf-8')

        self.send_header('Content-Length', len(out))
        self.end_headers()

        self.wfile.write(out)

    def send_json(self, content):

        content = json.dumps(content)

        out = bytearray(content, 'utf-8')

        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(out))
        self.end_headers()

        self.wfile.write(out)

class WatchDog(BlenderAddonDeveloperHTTPRequestHandler):

  router = { re.compile(k): v for k, v in {
      #    '/': default_route,
      r'^/script-path$': 'script_path_route',
      r'^/reload-addon/([^/]+)$': 'reload_addon_route',
  }.items() }

  def default_route(self):
    
      self.send_response(200)
      self.send_header('Content-Type', 'text/html')
      self.send_html("Blender Addon Developer")


  def script_path_route(self, path):

      global get_script_folder

      content = {
          'script_path': get_script_folder(),
      }

      self.send_response(200)
      self.send_json(content)
      
  def reload_addon_route(self, module):

      if module == 'rapido_developer':
        self.send_response(400)
        self.send_json({ 'reload': False, 'reason': 'rapido developer addon is excluded from reloads' })
        return

      module_folder = self.get_addon_folder(module)

      if not os.path.exists(module_folder):
        self.send_response(404)
        self.send_json({ 'reload': False, 'reason': f'addon {module} doesn\'t exist' })
        return

      Path('%s/__init__.py' % module_folder).touch()
      bpy.ops.preferences.addon_enable(module=module)

      self.send_response(200)
      self.send_json({ 'reload': True })

  def get_addon_folder(self, module):
      global get_script_folder
      return '%s/addons/%s' % (get_script_folder(), module)

  @staticmethod
  def get_http_server(os):

    if os == 'nt':
        MixIn = socketserver.ThreadingMixIn
    else:
        MixIn = socketserver.ForkingMixIn

    class MyHTTPServer(MixIn, HTTPServer):

        def finish_request(self, request, client_address):
            request.settimeout(15000)
            return HTTPServer.finish_request(self, request, client_address)

    return MyHTTPServer

  @staticmethod
  def get_server(os='_nix', fn=lambda: './dest', server_address=('localhost', 11111)):

      global get_script_folder
      get_script_folder = fn

      handler_class=__class__
      return __class__.get_http_server(os)(server_address, handler_class)


if __name__ == "__main__":
  try:
    print("serving at http://%s:%d" % server_address)
    srvr = WatchDog.get_server('nt', lambda: 'd:/Blender/.blender/scripts')
    srvr.serve_forever()
  except KeyboardInterrupt:
    srvr.socket.close()
