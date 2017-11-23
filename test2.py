import json
import requests


KEYWORD = 'yaml.load'
OPS_GERRIT_API = 'https://review.openstack.org'
GET_CHANGES_API = '/changes/?q=status:open&n=1000&o=CURRENT_REVISION&o=CURRENT_FILES'

r = requests.get("{}{}".format(OPS_GERRIT_API, GET_CHANGES_API))
changes = json.loads(r.content.replace(")]}'", "").strip())

f = open('links.txt', 'w+')

for change in changes:
    number = change['_number']
    change_id = change['change_id']
    print(change_id)
    revisions = change['revisions']
    current_revision_id = revisions.keys()[0]
    current_revision = revisions[current_revision_id]
    current_revision_number = current_revision['_number']
    for name in current_revision['files']:
        get_diff_api = "{}/changes/{}/revisions/{}/files/{}/diff".format(
           OPS_GERRIT_API, change_id, current_revision_id, name.replace('/', '%2F')
        )
        link = "{}/#/c/{}/{}/{}".format(
            OPS_GERRIT_API, number,
            current_revision_number, name
        )
        r = requests.get(get_diff_api)
        diff = r.content
        try:
            diff_dict = json.loads(diff.replace(")]}'", "").strip())
        except:
            continue
        list_change_parts = diff_dict.get('content')
        if isinstance(list_change_parts, list):
            for part in list_change_parts:
                # b: new code, a: code deleted, ab: not change
                new = part.get('b')
                if new and KEYWORD in new:
                    print(link)
                    f.write("{}\n".format(link))
f.close()
