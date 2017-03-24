#!/usr/bin/env python3
# -*- coding: utf8 -*-

# MIT License

# Copyright (c) 2017 Simon Wüllhorst

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
from JsonHandler import JsonHandler
from DataHandler import DataHandler
from GraphiteHandler import GraphiteHandler

def main():
    args = __parseArguments__()
    config = JsonHandler(args.config)
    rawJson = JsonHandler(args.hopglass_raw)
    rawType = DataHandler.TYPE_NODES_JSON if 'nodes' in rawJson.data else DataHandler.TYPE_RAW_JSON
        #detected nodes.json instead raw.json
    handler = DataHandler(rawJson.data, config.data, args.alternative_now, rawType)
    handler.convert()
    graphiteHandler = GraphiteHandler(config.data['graphite_target']['server'], config.data['graphite_target']['port'], args.alternative_now)
    graphiteHandler.prepareMessage(handler.domains, handler.nodes)
    # print(graphiteHandler.message)


def __parseArguments__():
    parser = argparse.ArgumentParser(description='This Script is a link between Hopglass-Server and Graphite.')
    parser.add_argument('-g', '--hopglass-raw', help='Hopglass raw.json source. Default: ./raw.json', default='./raw.json')
    parser.add_argument('-c', '--config', help='node-stats config file location Default: ./config.json', default='./config.json')
    parser.add_argument('-n', '--alternative-now', help='Set a fake now date.', required=False)
    parser.add_argument('-p', '--print-only', help='Print only', action='store_true')
    
    return parser.parse_args()

if __name__ == '__main__':
	main()