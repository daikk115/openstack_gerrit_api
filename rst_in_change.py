import json
import requests


OPS_GERRIT_API = 'https://review.openstack.org'
GET_CHANGES_API = '/changes/?q=status:open&n=1000&o=CURRENT_REVISION&o=CURRENT_FILES'

r = requests.get("{}{}".format(OPS_GERRIT_API, GET_CHANGES_API))
changes = json.loads(r.content.replace(")]}'", "").strip())


def get_changes(filename, keyword):
    f = open(filename, 'w+')

    for change in changes:
        number = change['_number']
        change_id = change['change_id']
        revisions = change['revisions']
        current_revision_id = revisions.keys()[0]
        current_revision = revisions[current_revision_id]
        current_revision_number = current_revision['_number']
        for name in current_revision['files']:
            if name.endswith('.rst'):
                link = "{}/#/c/{}".format(
                    OPS_GERRIT_API, number
                )
                f.write("{}\n".format(link))
                break
    f.close()


if __name__ == '__main__':
    # get_changes('iteritems.txt', '.iteritems')
    # get_changes('itervalues.txt', '.itervalues')
    # get_changes('iterkeys.txt', '.iterkeys')
    # get_changes('next.txt', '.next')
    # get_changes('basestring.txt', '.string_types')
    # get_changes('unicode.txt', '.text_type')
    # get_changes('func_name.txt', '.func_name')
    get_changes('rst.txt', 'assertRaisesRegexp')
