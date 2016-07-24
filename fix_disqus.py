from collections import OrderedDict
from sys import argv

from lxml.etree import parse
from twisted.python.filepath import FilePath



def main(wpImportFile, nikolaRoot):
    wpImportFile = FilePath(wpImportFile)
    nikolaRoot = FilePath(nikolaRoot)

    wpImport = parse(wpImportFile.open())
    for post in wpImport.iterfind('/channel/item'):
        if post.findtext('{http://wordpress.org/export/1.2/}status') != u'publish':
            continue
        updateDisqusId(disqusId(post), metaFile(nikolaRoot, post))



def disqusId(post):
    postId = post.findtext(u'{http://wordpress.org/export/1.2/}post_id')
    postGuid = post.findtext(u'guid')
    return u'{} {}'.format(postId, postGuid)



def metaFile(nikolaRoot, post):
    path = (
        post
        .findtext(u'link')
        .encode('ascii')
        .split('https://mithrandi.net/', 1)[1]
        .split('/'))
    return nikolaRoot.descendant(path).siblingExtension('.meta')



def updateDisqusId(did, mp):
    try:
        content = mp.getContent()
    except Exception as e:
        print e
        print 'Unable to update: ' + repr(mp)
        print 'DISQUS identifier: ' + repr(did)
    else:
        metadata = OrderedDict(
            line.split('.. ', 1)[1].split(': ', 1)
            for line in content.splitlines())
        if metadata.get('disqus_identifier', did) != did:
            print 'Refusing to overwrite different identifier in ' + repr(mp)
        else:
            metadata['disqus_identifier'] = did
            mp.setContent(''.join(
                '.. ' + ': '.join(item) + '\n'
                for item in metadata.iteritems()))



if __name__ == '__main__':
    main(*argv[1:])
