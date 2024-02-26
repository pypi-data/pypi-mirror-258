import argparse
from collections import defaultdict
import logging
import os
from sys import flags
from textwrap import indent
import yaml

from ..core import (
    set_wos_endpoint,
    get_wos_endpoint,
    CreateWSClient,
    wos_publish,
    wos_request,
    wos_env,
)
from ..utils import logger, enable_log
from ..type import WOSPublishMessage
import re, json, time


def print_api_result(res, err):
    if res != None:
        print(yaml.dump(res, indent=4))
    if err != None and err != "":
        print("ERROR:", err)


def pub(args):
    logger.info("Publishing resource=%s topic=%s", args.resource, args.topic)
    data = args.message
    dtype = False
    try:
        data = json.loads(data)
        logger.info("Convert message as json: %s", data)
        dtype = True
    except:
        dtype = False

    if not dtype:
        try:
            data = float(data)
            logger.info("Convert message as float: %f", float)
            dtype = True
        except:
            dtype = False

    if not dtype:
        try:
            data = int(data)
            logger.info("Convert message as int: %i", data)
            dtype = True
        except:
            dtype = False

    if not dtype:
        data = str(data)
        if str.lower(data) in ["true", "false"]:
            data = str.lower(data) == "true"
            logger.info("Convert message as boolean: %s", str(data))
    logger.info("message=%s", str(data))
    success, msg = wos_publish(args.resource, args.topic, data)
    logger.info("Publish success %s", success)
    print(yaml.dump(msg))


def req(args):
    res, err = wos_request(args.resource, args.action, args.data)
    if res != None:
        print(res)
    if err != None:
        print(err)


def act(args):
    client = CreateWSClient()
    client.connect()

    def fb(progress, status):
        print("feedback", progress, status)

    result, err = client.run_action(args.resource, args.action, args.data, fb)
    if result != None:
        print(result)
    if err != None:
        print(err)
    client.disconnect()


def sub(args):
    client = CreateWSClient()
    client.connect()

    def cb(msg: WOSPublishMessage):
        if args.topic != None and re.search(args.topic, msg.topic) == None:
            return
        print(yaml.dump(msg.to_json(), indent=2))
        if args.once:
            client.disconnect()
            exit(0)

    client.subscribe(args.resource, cb)


def hz(args):
    client = CreateWSClient()
    client.connect()
    counter = defaultdict(int)

    def cb(msg: WOSPublishMessage):
        if args.topic != None and re.search(args.topic, msg.topic) == None:
            return
        counter[msg.topic] += 1

    client.subscribe(args.resource, cb)
    while True:
        time.sleep(1)
        for k, c in counter.items():
            print(k, c, "hz")
        counter = defaultdict(int)


available_info = ["service", "env", "config", "robot", "component", "node", "graph"]


def info(args):

    if args.category == "service":
        print_api_result(*wos_request("core", "system-status", {}))
    if args.category == "env":
        print(yaml.dump(wos_env(), indent=2))
    if args.category == "config":
        print_api_result(*wos_request("config", "get-config", {}))
    if args.category == "robot":
        print_api_result(*wos_request("robot", "get-configs", {}))
    if args.category == "component":
        print_api_result(*wos_request("robot", "get-infos", {}))
    if args.category == "node":
        print_api_result(*wos_request("node", "get-nodes", {}))
    if args.category == "graph":
        result, err = wos_request("graph", "list-graphs", {})
        if err:
            print("ERROR", err)
            return
        for id in result:
            print(id, result[id]["name"], result[id]["description"])


def robot(args):

    if args.action == "start":

        _, err = wos_request("robot", "start", {})
        if err:
            print("ERROR", err)

    if args.action == "stop":
        _, err = wos_request("robot", "stop", {})
        if err:
            print("ERROR", err)


def parse_global_args():
    # Look for --endpoint in the argument list

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--endpoint",
        "-e",
        help="Set the endpoint environment variable",
        required=False,
    )
    parser.add_argument(
        "--verbose",
        help="Set verbose output",
        action="store_true",
    )
    # Parse known args returns the known arguments and any remaining arguments
    known_args, remaining_argv = parser.parse_known_args()
    if known_args.verbose:
        debug_level = os.getenv("DEBUG", False)
        if debug_level:
            enable_log(logging.DEBUG)
        else:
            enable_log(logging.INFO)

    if known_args.endpoint:
        os.environ["WOS_ENDPOINT"] = known_args.endpoint
        set_wos_endpoint(known_args.endpoint)

    return remaining_argv


handler = {
    "sub": sub,
    "pub": pub,
    "req": req,
    "act": act,
    "hz": hz,
    "info": info,
    "robot": robot,
}


def main():
    remaining_argv = parse_global_args()

    # Main parser
    parser = argparse.ArgumentParser(
        description="woscli - CLI tool to interact with WinGs Operating System"
    )

    parser.add_argument(
        "--endpoint",
        "-e",
        help="Set the endpoint environment variable",
        required=False,
    )
    parser.add_argument(
        "--verbose",
        help="Set verbose output",
        action="store_true",
    )

    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # subscribe
    parser_subscribe = subparsers.add_parser("sub", help="Subscribe to a resource")
    parser_subscribe.add_argument(
        "resource", type=str, help="Resource name to subscribe"
    )
    parser_subscribe.add_argument(
        "--topic", "-t", type=str, help="Optional topic filter", required=False
    )
    parser_subscribe.add_argument(
        "--once", action="store_true", help="Receive only once and exit"
    )

    # frequency
    parser_hz = subparsers.add_parser("hz", help="Calculate the publish frequency")
    parser_hz.add_argument("resource", type=str, help="Resource name to subscribe")
    parser_hz.add_argument(
        "--topic", "-t", type=str, help="Optional topic filter", required=False
    )

    # publish
    parser_publish = subparsers.add_parser("pub", help="Publish to a resource topic")
    parser_publish.add_argument("resource", type=str, help="Resource to publish to")
    parser_publish.add_argument("topic", type=str, help="Topic to publish to")
    parser_publish.add_argument("message", type=str, help="Data to publish")

    # request
    parser_request = subparsers.add_parser("req", help="Make a request")
    parser_request.add_argument("resource", type=str, help="Resource name for request")
    parser_request.add_argument("action", type=str, help="Action for request")
    parser_request.add_argument(
        "--data", type=str, help="Data for the request (optional)", required=False
    )

    # action
    parser_action = subparsers.add_parser("act", help="Perform an action")
    parser_action.add_argument("resource", type=str, help="Resource name for action")
    parser_action.add_argument("action", type=str, help="Action for action")
    parser_action.add_argument("data", type=str, help="Data for the action (optional)")

    # info
    parser_info = subparsers.add_parser("info", help="Get info about system")
    parser_info.add_argument(
        "category", type=str, help="Category of info", choices=available_info
    )

    # robot
    parser_robot = subparsers.add_parser("robot", help="Operation related to robot")
    parser_robot.add_argument(
        "action", type=str, help="Action to do", choices=["start", "stop"]
    )

    # Parse the remaining arguments
    args = parser.parse_args(remaining_argv)

    global handler

    if args.command in handler:
        logger.info("Using endpoint: %s", get_wos_endpoint())
        handler[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
