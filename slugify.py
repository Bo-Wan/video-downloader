# import unicodedata
#
# def slugify(value):
#     """
#     Normalizes string, converts to lowercase, removes non-alpha characters,
#     and converts spaces to hyphens.
#     """
#     value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
#     value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
#     value = unicode(re.sub('[-\s]+', '-', value))


import string

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
fileName = '285925850 Pillars/ Side Control Mastery Volume 7 by Stephen Whittier.mp4'
valid = ''.join(c for c in fileName if c in valid_chars)
print(fileName)
print(valid)
