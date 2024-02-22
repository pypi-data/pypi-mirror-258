#  /*
#   * MIT License
#   *
#   * Copyright (c) 2024 Gautam Sharma
#   *
#   * Permission is hereby granted, free of charge, to any person obtaining a copy
#   * of this software and associated documentation files (the "Software"), to deal
#   * in the Software without restriction, including without limitation the rights
#   * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   * copies of the Software, and to permit persons to whom the Software is
#   * furnished to do so, subject to the following conditions:
#   *
#   * The above copyright notice and this permission notice shall be included in all
#   * copies or substantial portions of the Software.
#   *
#   * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   * SOFTWARE.
#   */

#
# Created by Gautam Sharma on 2/19/24.
#


import grpc
import redislightning.redislite_pb2 as redislite_pb2
import redislightning.redislite_pb2_grpc as redislite_pb2_grpc

class Client:
    def __init__(self, port):
        self.port = port

    def init_connection(self):
        with grpc.insecure_channel("localhost:{}".format(self.port)) as channel:
            try:
                stub = redislite_pb2_grpc.RedisLiteServerStub(channel)
                # Generate random strings 200 times
                response = stub.InitConnection(redislite_pb2.InitRequest(connection_id="0.0.0.0:{}".format(self.port)))
                print("redis client status: " + response.status)
            except:
                print("Server not started");
                return

    def set(self, key, value):
        with grpc.insecure_channel("localhost:{}".format(self.port)) as channel:
            try:
                stub = redislite_pb2_grpc.RedisLiteServerStub(channel)
                # Generate random strings 200 times
                response = stub.Set(redislite_pb2.SetRequest(key=key, value=value))
                print("redis client status: " + response.status)
            except:
                print("Server not started");
                return

    def get(self, key):
        with grpc.insecure_channel("localhost:{}".format(self.port)) as channel:
            try:
                stub = redislite_pb2_grpc.RedisLiteServerStub(channel)
                # Generate random strings 200 times
                response = stub.Get(redislite_pb2.GetRequest(key=key))
                print("redis client status: " + response.status)
                if(response.status == "REDISLITE_OK"):
                    print("Got value " + response.status)
                    return response.value
                else:
                    print("Key not found")

            except:
                print("Server not started");
                return