import json
import requests


KEYWORD = 'objects'
OPS_GERRIT_API = 'https://review.openstack.org'
GET_CHANGES_API = '/changes/?q=status:open&n=100&o=CURRENT_REVISION&o=CURRENT_FILES'

r = requests.get("{}{}".format(OPS_GERRIT_API, GET_CHANGES_API))
changes = json.loads(r.content.replace(")]}'", "").strip())

for change in changes:
    number = change['_number']
    change_id = change['change_id']
    revisions = change['revisions']
    current_revision_id = revisions.keys()[0]
    current_revision = revisions[current_revision_id]
    for name in current_revision['files']:
        name = name.replace('/', '%2F')
        get_diff_api = "{}/changes/{}/revisions/{}/files/{}/diff".format(
           OPS_GERRIT_API, change_id, current_revision_id, name
        )
        r = requests.get(get_diff_api)
        diff = r.content
        if KEYWORD in diff:
            print("{}/#/c/{}/".format(
                OPS_GERRIT_API, number
            ))
