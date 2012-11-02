# -*- coding: utf-8 -*-
import logging
if __name__ == '__main__':
    logging.basicConfig()
_log = logging.getLogger(__name__)
import pyxb
import pyxb.binding.generate
import pyxb.utils.domutils
import pyxb.binding.saxer
import StringIO

from xml.dom import Node

import os.path
schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../schemas/xsi-nil.xsd'))
code = pyxb.binding.generate.GeneratePython(schema_location=schema_path)

rv = compile(code, 'test', 'exec')
eval(rv)

from pyxb.exceptions_ import *

import unittest

def setFull (instance, value):
    instance.full = value
    return instance

class TestXSIType (unittest.TestCase):

    def testFull (self):
        xml = '<full xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">content</full>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, 'content')
        self.assertFalse(instance._isNil())
        self.assertRaises(pyxb.NoNillableSupportError, instance._setIsNil)

        xml = '<full xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="false">content</full>'
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, 'content')
        self.assertFalse(instance._isNil())

        xml = '<full xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true">content</full>'
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, 'content')
        self.assertFalse(instance._isNil())


    def testXFull (self):
        xml = '<xfull xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">content</xfull>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, 'content')
        self.assertFalse(instance._isNil())
        self.assertRaises(pyxb.NoNillableSupportError, instance._setIsNil)

    def testOptional (self):
        xml = '<optional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">content</optional>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, 'content')
        self.assertFalse(instance._isNil())
        instance._setIsNil()
        self.assertTrue(instance._isNil())

        saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace)
        handler = saxer.getContentHandler()
        saxer.parse(StringIO.StringIO(xml))
        instance = handler.rootObject()
        self.assertEqual(instance, 'content')
        self.assertFalse(instance._isNil())


    def testOptionalNilFalse (self):
        xml = '<optional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="false">content</optional>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, 'content')
        self.assertFalse(instance._isNil())
        instance._setIsNil()
        self.assertTrue(instance._isNil())

    def testOptionalNilEETag (self):
        xml = '<optional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, '')
        self.assertTrue(instance._isNil())

        saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace)
        handler = saxer.getContentHandler()
        saxer.parse(StringIO.StringIO(xml))
        instance = handler.rootObject()
        self.assertEqual(instance, '')
        self.assertTrue(instance._isNil())

    def testOptionalNilSETag (self):
        xml = '<optional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"></optional>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, '')
        self.assertTrue(instance._isNil())

        saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace)
        handler = saxer.getContentHandler()
        saxer.parse(StringIO.StringIO(xml))
        instance = handler.rootObject()
        self.assertEqual(instance, '')
        self.assertTrue(instance._isNil())

    def testOptionalNilSCETag (self):
        xml = '<optional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"><!-- comment --></optional>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, '')
        self.assertTrue(instance._isNil())

        saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace)
        handler = saxer.getContentHandler()
        saxer.parse(StringIO.StringIO(xml))
        instance = handler.rootObject()
        self.assertEqual(instance, '')
        self.assertTrue(instance._isNil())

    def testNilOptionalSpaceContent (self):
        xml = '<optional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"> </optional>'
        self.assertRaises(pyxb.ContentInNilInstanceError, CreateFromDocument, xml)

    def testNilComplexSpaceContent (self):
        xml = '<complex xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"> </complex>'
        self.assertRaises(pyxb.ContentInNilInstanceError, CreateFromDocument, xml)

    def testComplexInternal (self):
        xml = '<complex><full>full content</full><optional>optional content</optional></complex>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance.full, 'full content')
        self.assertEqual(instance.optional, 'optional content')
        self.assertFalse(instance.optional._isNil())
        self.assertEqual(instance.toDOM().documentElement.toxml("utf-8"), xml)
        instance.validateBinding()

        saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace)
        handler = saxer.getContentHandler()
        saxer.parse(StringIO.StringIO(xml))
        instance = handler.rootObject()
        self.assertEqual(instance.full, 'full content')
        self.assertEqual(instance.optional, 'optional content')
        self.assertFalse(instance.optional._isNil())

        xml = '<complex xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><full>full content</full><optional xsi:nil="true"></optional></complex>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance.full, 'full content')
        self.assertEqual(instance.optional, '')
        self.assertTrue(instance.optional._isNil())
        self.assertEqual(instance.toDOM().documentElement.toxml("utf-8"), xml)
        instance.validateBinding()

        saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace)
        handler = saxer.getContentHandler()
        saxer.parse(StringIO.StringIO(xml))
        instance = handler.rootObject()
        self.assertEqual(instance.full, 'full content')
        self.assertEqual(instance.optional, '')
        self.assertTrue(instance.optional._isNil())

        xml = '<complex xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>'
        instance._setIsNil()
        self.assertEqual(instance.toDOM().documentElement.toxml("utf-8"), xml)
        instance.validateBinding()

    def testComplex (self):
        canonical = '<complex xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>'
        for xml in ( canonical,
                     '<complex xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"></complex>',
                     '<complex xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"><!-- comment --></complex>') :
            doc = pyxb.utils.domutils.StringToDOM(xml)
            instance = CreateFromDOM(doc.documentElement)
            self.assertTrue(instance._isNil())
            self.assertEqual(instance.toDOM().documentElement.toxml("utf-8"), canonical)
            instance.validateBinding()

    def testConstructorNil (self):
        o = optional()
        self.assertFalse(o._isNil())
        o = optional(_nil=True)
        self.assertTrue(o._isNil())
        c = complex()
        self.assertFalse(c._isNil())
        c = complex(_nil=True)
        self.assertTrue(c._isNil())
        s = simple()
        self.assertFalse(s._isNil())
        s = simple(_nil=True)
        self.assertTrue(s._isNil())

    def testNilSetAndAppend (self):
        s = simple(_nil=True)
        self.assertRaises(pyxb.ContentInNilInstanceError, s.append, 'one')
        c = complex(_nil=True)
        self.assertRaises(pyxb.ContentInNilInstanceError, c.append, 'one')
        full = c._UseForTag('full')
        self.assertRaises(pyxb.ContentInNilInstanceError, setFull, c, 'yes')
        self.assertRaises(pyxb.ContentInNilInstanceError, full.append, c, 'yes')
        self.assertRaises(pyxb.ContentInNilInstanceError, full.setOrAppend, c, 'yes')
        multi = c._UseForTag('multi')
        self.assertRaises(pyxb.ContentInNilInstanceError, multi.append, c, 'one')
        self.assertRaises(pyxb.ContentInNilInstanceError, multi.setOrAppend, c, 'one')
        # Nothing we can do about assignments that bypass the validation hooks.
        # Customizing list would probably destroy performance.
        c.multi.append('one')

if __name__ == '__main__':
    unittest.main()
    
        
