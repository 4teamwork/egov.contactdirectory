import os.path
import ldif


def get_ldif_records(filename):
    path = os.path.join(os.path.dirname(__file__), 'data', filename)
    rlist = ldif.LDIFRecordList(open(path, 'rb'))
    rlist.parse()
    return rlist.all_records
