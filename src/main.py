import logging
import sys
import os

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def main(rpc_user, rpc_password, rpc_host, rpc_port):
    logging.basicConfig()
    logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)
    rpc_connection = AuthServiceProxy(
        "http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_host, rpc_port),
        timeout=120)
    best_block_hash = rpc_connection.getbestblockhash()
    print(rpc_connection.getblock(best_block_hash))

    # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
    commands = [ [ "getblockhash", height] for height in range(100) ]
    block_hashes = rpc_connection.batch_(commands)
    blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
    block_times = [ block["time"] for block in blocks ]
    print(block_times)

if __name__ == "__main__":
    rpc_user = str(sys.argv[1])
    rpc_password = str(sys.argv[2])
    rpc_host = str(sys.argv[3])
    rpc_password = str(sys.argv[4])
    main(rpc_user, rpc_password, rpc_host, rpc_password)
