import snakebite.client as client
import snakebite.protobuf.ClientNamenodeProtocol_pb2 as client_proto
from snakebite.channel import DataXceiverChannel
import Queue


#client._get_dir_listing('/')
#cl.cat('/wikipedia')
#list(cl.ls(['/']))

def create_client(hostname, port):
    return client.Client(hostname, port=port)

def get_locations(blocks):
    return set(loc.id.ipAddr for block in blocks for loc in block.locs)


def read_block(block):
    location = block.locs[0]
    host = location.id.ipAddr
    port = int(location.id.xferPort)
    data_xciever = DataXceiverChannel(host, port)
    if not data_xciever.connect():
        return
    offset_in_block = 0
    check_crc = False
    length = block.b.numBytes
    block_gen = data_xciever.readBlock(length, block.b.poolId, block.b.blockId, block.b.generationStamp, offset_in_block, check_crc)
    return block_gen


def find_blocks(client, path):
    fileinfo = client._get_file_info(path)
    node = fileinfo.fs
    length = node.length
    request = client_proto.GetBlockLocationsRequestProto()
    request.src = path
    request.length = length
    request.offset = 0L
    response = client.service.getBlockLocations(request)
    return list(response.locations.blocks)


def find_out_things(client, path, tail_only=False, check_crc=False):
    fileinfo = client._get_file_info(path)
    node = fileinfo.fs
    length = node.length
    print "Length: ", length

    request = client_proto.GetBlockLocationsRequestProto()
    request.src = path
    request.length = length

    if tail_only:  # Only read last KB
        request.offset = max(0, length - 1024)
    else:
        request.offset = 0L
    response = client.service.getBlockLocations(request)

    lastblock = response.locations.lastBlock

    #if tail_only:
    #    if lastblock.b.blockId == response.locations.blocks[0].b.blockId:
    #        num_blocks_tail = 1  # Tail is on last block
    #    else:
    #        num_blocks_tail = 2  # Tail is on two blocks

    failed_nodes = []
    total_bytes_read = 0
    for block in response.locations.blocks:
        length = block.b.numBytes
        pool_id = block.b.poolId
        print "Length: %s, pool_id: %s" % (length, pool_id)
        offset_in_block = 0
        if tail_only:
            if num_blocks_tail == 2 and block.b.blockId != lastblock.b.blockId:
                offset_in_block = block.b.numBytes - (1024 - lastblock.b.numBytes)
            elif num_blocks_tail == 1:
                offset_in_block = max(0, lastblock.b.numBytes - 1024)
        # Prioritize locations to read from
        locations_queue = Queue.PriorityQueue()  # Primitive queuing based on a node's past failure
        for location in block.locs:
            if location.id.storageID in failed_nodes:
                locations_queue.put((1, location))  # Priority num, data
            else:
                locations_queue.put((0, location))

        # Read data
        successful_read = False
        while not locations_queue.empty():
            location = locations_queue.get()[1]
            host = location.id.ipAddr
            port = int(location.id.xferPort)
            data_xciever = DataXceiverChannel(host, port)
            if data_xciever.connect():
                try:
                    for load in data_xciever.readBlock(length, pool_id, block.b.blockId, block.b.generationStamp, offset_in_block, check_crc):
                        offset_in_block += len(load)
                        total_bytes_read += len(load)
                        successful_read = True
                        yield load
                except Exception, e:
                    log.error(e)
                    if not location.id.storageID in failed_nodes:
                        failed_nodes.append(location.id.storageID)
                    successful_read = False
            else:
                raise Exception
            if successful_read:
                break
        if successful_read is False:
            raise Exception("Failure to read block %s" % block.b.blockId)
