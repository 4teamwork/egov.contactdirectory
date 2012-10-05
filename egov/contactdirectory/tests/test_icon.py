from unittest2 import TestCase
from egov.contactdirectory.browser.helper import icon


class IconTestCase(TestCase):

    def test_noumlauts(self):
        item = {'url':'http://blubb.ch', 'icon':'hans_peter'}
        html = icon(item, 'hans muster')
        self.assertEqual(html, u'<a href="http://blubb.ch">hans_peterhans muster</a>')

    def test_umlauts(self):
        item = {'url':'http://blubb.ch', 'icon':'hans_peter'}
        html = icon(item, 'h\xc3\xa4ns m\xc3\xbcster')
        self.assertEqual(html, u'<a href="http://blubb.ch">hans_peterh\xe4ns m\xfcster</a>')

    def test_unicode(self):
        item = {'url':'http://blubb.ch', 'icon':'hans_peter'}
        html = icon(item, 'h\xc3\xa4ns m\xc3\xbcster'.decode('utf-8'))
        self.assertEqual(html, u'<a href="http://blubb.ch">hans_peterh\xe4ns m\xfcster</a>')
