from base64 import b64encode
from plone.namedfile.utils import stream_data
from StringIO import StringIO


def generateVCard(contact):

    io = StringIO()

    gender_map = {
        'm': 'M',
        'f': 'F',
        '': 'U'
    }

    def addProp(name, value):
        if value not in (None, '', u''):
            io.write('{0}:{1}\n'.format(name, value))

    addProp('BEGIN', 'VCARD')
    addProp('VERSION', '3.0')
    addProp('N', '{0};{1};;{2}'.format(contact.getLastname(),
                                       contact.getFirstname(),
                                       contact.getSalutation()))
    addProp('FN', contact.Title())
    addProp('GENDER', gender_map.get(contact.getGender(), ''))
    addProp('ORG', contact.getOrganization())
    addProp('ADR;TYPE=WORK', ';;{0};{1};;{2};{3}'.format(
        contact.getAddress().replace('\n', '\\n').replace('\r', ''),
        contact.getCity(),
        contact.getZip(),
        contact.getCountry()))
    addProp('EMAIL', contact.getEmail())
    addProp('TEL;TYPE=WORK', contact.getPhone_office())
    addProp('TEL;TYPE=WORK;TYPE=CELL', contact.getPhone_mobile())
    addProp('TEL;TYPE=WORK;TYPE=FAX', contact.getFax())
    addProp('URL', contact.getWww())
    addProp('ROLE', contact.getFunction())
    addProp('TEL;TYPE=HOME', contact.getTel_private())
    addProp('ADR;TYPE=HOME', ';;{0};{1};;{2};'.format(
        contact.getAddress_private().replace('\r\n', '\\n').replace('\r', ''),
        contact.getCity_private(),
        contact.getZip_private()))

    if contact.getImage():
        imgdata = StringIO()
        imgdata.write(stream_data(contact.getImage()))
        addProp('PHOTO;ENCODING=B', b64encode(imgdata.getvalue()))

    addProp('END', 'VCARD')
    io.seek(0)

    return io
