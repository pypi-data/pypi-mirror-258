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

from __future__ import print_function
import logging
import redislightning as redislightning


def run():
    c = redislightning.RedisLightningClient(50051)
    c.init_connection()
    for idx in range(1,10):
        k = input("Set Key ")
        v = input("Set Value ")
        c.set(k, v)
        cached_val = c.get(k)
        print("Cached value of key {} is {}".format(k, cached_val))



if __name__ == "__main__":
    logging.basicConfig()
    run()