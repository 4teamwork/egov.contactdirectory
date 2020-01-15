# -*- coding: utf-8 -*-
from egov.contactdirectory.testing import \
    EGOV_CONTACTDIRECTORY_FUNCTIONAL_TESTING
from egov.contactdirectory.vcard import generateVCard
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from StringIO import StringIO
from unittest import TestCase
from zipfile import ZipFile
import os


def asset(filename):
    here = os.path.dirname(__file__)
    path = os.path.join(here, 'assets', filename)
    with open(path, 'r') as file_:
        return file_.read()


class ExportTest(TestCase):

    layer = EGOV_CONTACTDIRECTORY_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        self.detailed_contact = create(Builder('contact').having(
            organization=u'Fant\xe0storg',
            gender='f',
            lastname=u'M\xe9ier',
            firstname=u'Fr\xedtz',
            address=u'Chrache zw\xf6i',
            zip='1337',
            city=u'G\xf4tham',
            country='Schweiz',
            email='fmeier@stirnimaa.ch',
            phone_office='+41 33 456 78 01',
            phone_mobile='+70 98 765 43 21',
            fax='+41 33 456 78 02',
            www='http://www.cheib.ch',
            academic_title='Master of the Universe',
            function=u'Imk\xe9r',
            department=u'Cust\xf5mer Services',
            salutation='Sir',
            text=u'He is \xb1 awesome!',
            tel_private='+41 70 123 32 12',
            address_private='Chriesleweg 5',
            zip_private='9999',
            city_private='Dubai')
            .with_photo())

        self.minimal_contact = create(Builder('contact').having(
            lastname='Blau',
            firstname='Minho'))

    def test_vcf_generation(self):
        vcf_meier = generateVCard(self.detailed_contact).getvalue()
        self.assertMultiLineEqual(asset('fritz-meier.vcf'), vcf_meier)

        vcf_blau = generateVCard(self.minimal_contact).getvalue()
        self.assertMultiLineEqual(asset('blau-minho.vcf'), vcf_blau)

    @browsing
    def test_zip_export(self, browser):
        browser.login().visit(self.detailed_contact, view='zip_export')
        self.assertEquals('application/zip', browser.headers['Content-Type'])

        zipfile = ZipFile(StringIO(browser.contents))
        self.assertEquals(['contact.vcf'], zipfile.namelist())
        self.assertMultiLineEqual(asset('fritz-meier.vcf'),
                                  zipfile.read('contact.vcf'))
