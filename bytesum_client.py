import hdfs_fun

import json
import requests
import sys

def get_bytesum_request(ip, port, pool_id, block_id):
    url = "http://{url}:{port}".format(url=ip,port=port)
    payload = {"pool_id" : pool_id, "block_id": block_id}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print r.text

def remote_filename(block):
    return "/mnt/var/lib/hadoop/dfs/current/{pool_id}/current/finalized/blk_{block_id}".format(pool_id=pool_id,
            block_id=block_id)


if __name__ == "__main__":
    filename = sys.argv[1]
    cl = hdfs_fun.create_client()
    blocks = hdfs_fun.find_blocks(cl, filename)
    for block in blocks:
        location = block.locs[0]
        host = location.id.ipAddr
        pool_id = block.b.poolId
        block_id = block.b.blockId
        get_bytesum_request(host, 8080, pool_id, block_id)
