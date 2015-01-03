#!/usr/bin/env python3
from http.client import HTTPConnection
from urllib.parse import urlencode
from gi.repository import Gtk


class ClientTestHTTP(object):

    def __init__(self, host='127.0.0.1', port=None):
        self._connection=HTTPConnection(host, port)
        self._host=host
        self._codes={}
        self._responses=[]

    def request(self, method='GET', path='/', host=None, headers={}, data=None, log=print):
        # Connect
        try:
            self._connection.connect()
        except:
            log('Error in connection\n')
            return
        log('Connected')
        # Start request
        self._connection.putrequest(method, path, True)
        log(method + ' ' + path)
        # Set host header
        if host is None:
            self._connection.putheader('Host', self._host)
            log('Host: ' + self._host)
        else:
            self._connection.putheader('Host', host)
            log('Host: ' + host)
        # Set all headers
        for header, value in headers.items():
            if header == 'Host':
                continue
            self._connection.putheader(header, value)
            log(header + ': ' + value)
        self._connection.endheaders()
        log('')
        # Send body data if exist
        if not data is None:
            # If data is a dict (for example for POST request)
            if type(data) is dict:
                data = urlencode(data)
            self._connection.send(data)
        # Get response
        response = self._connection.getresponse()
        # Close connection
        self._connection.close()
        # Stats of status codes
        if not response.status in self._codes:
            self._codes[response.status]=1
        else:
            self._codes[response.status]=self._codes[response.status]+1
        # Append response
        self._responses.append(response)
        log("Status: %i" % response.status)
        for header, value in response.getheaders():
            log(header + ': ' + value)
        log('')


class BufferWrapper(object):

    def __init__(self, gtk_buffer):
        self.buffer = gtk_buffer

    def write(self, text):
        self.buffer.insert_at_cursor(text + '\n')


class GUI(object):

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def sendRequest(self, button):
        # Get data from GTK widgets
        ip = self.builder.get_object('ipaddress').get_text()
        port = self.builder.get_object('port').get_text()
        method = self.builder.get_object('method').get_text()
        path = self.builder.get_object('path').get_text()
        host = self.builder.get_object('host').get_text()
        # Send request
        client=ClientTestHTTP(ip, port)
        client.request(method, path, host, log=self.log.write)

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('ClientTestHTTPGUI.glade')
        self.builder.connect_signals(self)
        self.log = BufferWrapper(self.builder.get_object('logtextview').get_buffer())
        self.window = self.builder.get_object('mainwindow')
        self.window.show_all()
        Gtk.main()

# Start GUI
GUI()
