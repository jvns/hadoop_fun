import hdfs_fun

import json
import requests
import sys

def get_bytesum_request(ip, port, filename):
    url = "http://{url}:{port}".format(url=ip,port=port)
    payload = {"filename" : filename}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print r.text

def remote_filename(block):
    pass

if __name__ == "__main__":
    filename = sys.argv[1]
    cl = hdfs_fun.create_client()
    blocks = hdfs_fun.find_blocks(cl, filename)
    for block in blocks:
        location = block.locs[0]
        host = location.id.ipAddr
        get_bytesum_request(host, 8080, filename)
