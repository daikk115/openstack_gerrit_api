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
        #print(change_id, keyword)
        revisions = change['revisions']
        current_revision_id = revisions.keys()[0]
        current_revision = revisions[current_revision_id]
        current_revision_number = current_revision['_number']
        for name in current_revision['files']:
            get_diff_api = "{}/changes/{}/revisions/{}/files/{}/diff".format(
               OPS_GERRIT_API, change_id, current_revision_id, name.replace('/', '%2F')
            )
            r = requests.get(get_diff_api)
            diff = r.content
            if keyword in diff:
                link = "{}/#/c/{}/{}/{}".format(
                    OPS_GERRIT_API, number,
                    current_revision_number, name
                )
                print(link)
                f.write("{}\n".format(link))
    f.close()


if __name__ == '__main__':
    # get_changes('iteritems.txt', '.iteritems')
    # get_changes('itervalues.txt', '.itervalues')
    # get_changes('iterkeys.txt', '.iterkeys')
    # get_changes('next.txt', '.next')
    # get_changes('basestring.txt', '.string_types')
    # get_changes('unicode.txt', '.text_type')
    # get_changes('func_name.txt', '.func_name')
    get_changes('links.txt', 'import')
