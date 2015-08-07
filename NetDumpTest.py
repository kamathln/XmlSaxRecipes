# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import xml.sax,sys
from XmlSaxDump import XmlSaxDumper
import socket
import SocketServer


class XmlStreamDumpServer(SocketServer.StreamRequestHandler):
    def handle(self):
        print ("<!-- New connection -->")
        parser=xml.sax.make_parser()
        parser.setFeature(xml.sax.expatreader.feature_external_ges, 0)
        parser.setFeature(xml.sax.handler.feature_namespaces, 1)
        parser.document_closed = False
        xmlevent_handler = XmlSaxDumper()
        xmlevent_handler.setParser(parser)
        parser.setContentHandler(xmlevent_handler)
        while True:
            rcvd=self.request.recv(256)
            parser.feed(rcvd)
            if parser.document_closed:
                parser.close()
                break

if __name__ == '__main__':
    tcpserver =SocketServer.TCPServer(('0.0.0.0',int(sys.argv[1])),XmlStreamDumpServer)
    #serversocket = socket.socket()
    tcpserver.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    tcpserver.serve_forever() 
