# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import xml.sax
from xml.sax.saxutils import quoteattr as qa, escape

class XmlSaxDumper(xml.sax.ContentHandler):
    def setParser(self,parser):
        self.parser=parser
    def startDocument(self):
        print ("<Document>")
    def startElement(self,name,attrs):
        print ("<Element name=%s>" % (qa(name)))
        for (ak,av) in attrs.items():
            print ("<Attribute name=%s>%s</Attribute>" % ( qa(ak), escape(av) ) ) 
    def startElementNS(self, name, qname, attrs):
        print ("<ElementNS name=%s namespace=%s qname=%s>" %(qa(str(name[1])),qa(str(name[0])), qa(str(qname))))
        for (ak,av) in attrs.items():
            print ("<Attribute name=%s>%s</Attribute>" % ( qa(str(ak)), escape(str(av)) ) ) 

    def startPrefixMapping (self, prefix, uri):
        print ("<PrefixMapping prefix=%s uri=%s>" % (qa(str(prefix)), qa(str(uri))))
    def endPrefixMapping(self, prefix):
        print ("</PrefixMapping><!-- %s -->" % qa(str(prefix)))
    def endElementNS(self, name, qname):
        print ("</ElementNS><!-- name=%s qname=%s -->" %(qa(str(name)), qa(str(qname)))) 
    def endElement(self, name):
        print ("</Element><!-- name=%s>" % qa(name))
    def endDocument(self):
        print ("</Document>")
        try:
            self.parser.document_closed=True
        except:
            pass
    def characters(self,chs):
        print ("<![CDATA[%s]]>" % (escape(chs)))

if __name__ == '__main__':
    reader = xml.sax.make_parser()
    reader.setFeature(xml.sax.expatreader.feature_external_ges,0)
#    reader.setFeature(xml.sax.expatreader.feature_namespace_prefixes,1)
    reader.setContentHandler(XmlSaxDumper())
    
    if len(sys.argv) == 2:
        reader.parse(sys.argv[1])
    else:
        reader.parse(sys.stdin)
