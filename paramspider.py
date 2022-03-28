#!/usr/bin/env python3
import argparse
import os
import re
import sys
import time
import urllib.parse
from urllib.parse import unquote

import requests
from loguru import logger

from core import requester

start_time = time.time()
version = "2"


def fastextract(response, black_list):
    return [
        line
        for line in response.split("\n")
        if "?" in line
        if not any(bad in line for bad in black_list)
    ]


def main():
    logger.remove()
    logger.add(
        sys.stdout,
        level="DEBUG",
        colorize=True,
        format="<green>{time:HH:mm:ss}</green> <level>{message}</level>",
    )
    logger.add(
        sys.stdout,
        level="INFO",
        colorize=True,
        format="<green>{time:HH:mm:ss}</green> <level>{message}</level>",
    )

    logger.debug(f"ParamSpider v{version} by Devansh Batham (devanshbatham), forked by Jake0x48 <3")
    logger.debug("starting now :)")

    if not os.path.isdir("output"):
        os.mkdir("output")

    parser = argparse.ArgumentParser(
        description="ParamSpider a parameter discovery suite"
    )
    parser.add_argument(
        "-d",
        "--domain",
        help="Domain name of the taget [ex : hackerone.com]",
        required=True,
    )
    parser.add_argument(
        "-s", "--subs", help="Set False for no subs [ex : --subs False ]", default=True
    )
    parser.add_argument(
        "-e", "--exclude", help="extensions to exclude [ex --exclude php,aspx]"
    )
    parser.add_argument(
        "-o", "--output", help="Output file name [by default it is 'domain.txt']"
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="Do not print the results to the screen",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--retries",
        help="Specify number of retries for 4xx and 5xx errors",
        default=3,
    )
    args = parser.parse_args()

    if args.subs == True or " True":
        url = f"https://web.archive.org/cdx/search/cdx?url=*.{args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    else:
        url = f"https://web.archive.org/cdx/search/cdx?url={args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"

    retry = True
    retries = 0
    while retry == True and retries <= int(args.retries):
        response, retry = requester.connector(url)
        retry = retry
        retries += 1
    if response == False:
        return
    response = unquote(response)

    # for extensions to be excluded
    black_list = []
    if args.exclude:
        if "," in args.exclude:
            black_list = args.exclude.split(",")
            for i in range(len(black_list)):
                black_list[i] = "." + black_list[i]
        else:
            black_list.append("." + args.exclude)

    else:
        black_list = []  # for blacklists
    if args.exclude:
        logger.debug(
            f"urls containing these extensions will be excluded from the results: {black_list}"
        )

    fast_uris = fastextract(response, black_list)

    urls = "\n".join(sorted(set(fast_uris)))
    final_urls = urls.replace(" ", "+")

    if not args.quiet:
        print(final_urls)

    logger.debug(f"total number of retries: {retries-1}")
    logger.debug(f"total unique urls found: {len(fast_uris)}")
    if args.output:
        if "/" in args.output:
            logger.debug(f"output is saved here: {args.output}")
            with open(f"{args.output}.txt", "wt", encoding="utf-8") as file:
                file.write(final_urls)
        else:
            logger.debug(f"output is saved here: output/{args.output}")
            with open(f"output/{args.output}", "wt", encoding="utf-8") as file:
                file.write(final_urls)
    else:
        logger.debug(f"output is saved here: output/{args.domain}.txt")
        with open(f"output/{args.domain}.txt", "wt", encoding="utf-8") as file:
            file.write(final_urls)
    logger.debug(f"total execution time: {str((time.time() - start_time))[:-12]}")


if __name__ == "__main__":
    main()
