def icon(item, value):
    url_method = lambda: '#'
    href = item.get('url', url_method())
    if not item.get('icon'):
        return u'<a href="%s">%s</a>' % (href.decode('utf8'), value)
    return u'<a href="%s">%s%s</a>' % (href.decode('utf8'), item.get('icon'), value)
