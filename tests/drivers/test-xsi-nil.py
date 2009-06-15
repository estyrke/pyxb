import pyxb
import pyxb.binding.generate
import pyxb.utils.domutils
import pyxb.binding.saxer
import StringIO

from xml.dom import Node

import os.path
schema_path = '%s/../schemas/xsi-nil.xsd' % (os.path.dirname(__file__),)
code = pyxb.binding.generate.GeneratePython(schema_file=schema_path)

rv = compile(code, 'test', 'exec')
eval(rv)

from pyxb.exceptions_ import *

import unittest

class TestXSIType (unittest.TestCase):
    def testFull (self):
        xml = '<full xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">content</full>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, 'content')
        self.assertRaises(pyxb.NoNillableSupportError, instance._isNil)
        self.assertRaises(pyxb.NoNillableSupportError, instance._setIsNil)

    def testXFull (self):
        xml = '<xfull xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">content</xfull>'
        doc = pyxb.utils.domutils.StringToDOM(xml)
        instance = CreateFromDOM(doc.documentElement)
        self.assertEqual(instance, 'content')
        self.assertRaises(pyxb.NoNillableSupportError, instance._isNil)
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

    def testOptionalNil (self):
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


if __name__ == '__main__':
    unittest.main()
    
        
