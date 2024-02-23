import argparse
import asyncio
import aiofiles
import aiodns
import logging
import platform
from collections.abc import Awaitable
from pathlib import Path


logger = logging.getLogger("makima")


def file_exists(filename: str) -> Path:
    path = Path(filename)

    if not path.is_file():
        raise FileNotFoundError

    return path


async def record_lookup(resolver: aiodns.DNSResolver,
                        subdomain: str,
                        record_type: str) -> Awaitable:
    logger.info(f"Looking up {record_type} records for {subdomain}")

    try:
        return await resolver.query(subdomain, record_type)
    except aiodns.error.DNSError as error:
        logger.warning(f"aiodns error: {error}")
    except Exception as error:
        logger.error(f"Unexpected error: {error}")


async def a_record_lookup(resolver: aiodns.DNSResolver,
                          subdomain: str) -> Awaitable:
    return await record_lookup(resolver, subdomain, "A")


async def aaaa_record_lookup(resolver: aiodns.DNSResolver,
                             subdomain: str) -> Awaitable:
    return await record_lookup(resolver, subdomain, "AAAA")


async def mx_record_lookup(resolver: aiodns.DNSResolver,
                           subdomain: str) -> Awaitable:
    return await record_lookup(resolver, subdomain, "MX")


async def ns_record_lookup(resolver: aiodns.DNSResolver,
                           subdomain: str) -> Awaitable:
    return await record_lookup(resolver, subdomain, "NS")


async def bruteforce(domain: str, wordlist: Path) -> None:
    logger.debug("Creating DNS resolver")

    resolver = aiodns.DNSResolver()

    logger.debug(f"Asynchronously iterating over wordlist {wordlist}")

    async with aiofiles.open(wordlist, mode="r") as wordlist_file:
        async for line in wordlist_file:
            subdomain = line.strip() + "." + domain

            logger.debug(f"Crafted subdomain {subdomain}")

            a_records = await a_record_lookup(resolver, subdomain)
            aaaa_records = await aaaa_record_lookup(resolver, subdomain)
            mx_records = await mx_record_lookup(resolver, subdomain)
            ns_records = await ns_record_lookup(resolver, subdomain)
            records_list = [a_records, aaaa_records, mx_records, ns_records]
            addresses = list()

            for records in records_list:
                if records is not None:
                    addresses.extend([record.host for record in records])

            if len(addresses) > 0:
                addresses_string = " ".join(addresses)

                logger.info(
                    f"Retrieved records for {subdomain}: {addresses_string}")

                print(f"{subdomain} {addresses_string}")


def main():
    parser = argparse.ArgumentParser(
        description="Makima - Asynchronous DNS Brute Forcer by irisdotsh")

    parser.add_argument("domain", help="Root domain")
    parser.add_argument("wordlist",
                        type=file_exists,
                        help="Wordlist used for generating subdomains")
    parser.add_argument("-v",
                        "--verbose",
                        action="count",
                        default=0,
                        help="Verbosity")

    args = parser.parse_args()

    level = logging.ERROR

    match args.verbose:
        case 0:
            level = logging.ERROR
        case 1:
            level = logging.WARNING
        case 2:
            level = logging.INFO
        case 3:
            level = logging.DEBUG

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.setLevel(level)

    logger.debug("Checking OS")

    os = platform.system()

    if os == "Windows":
        logger.debug("Windows OS detected, setting event loop policy")

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    domain = args.domain
    wordlist = args.wordlist

    logger.info(
        f"Bruteforcing A records for {domain} with wordlist {wordlist}")

    asyncio.run(bruteforce(domain, wordlist))


if __name__ == "__main__":
    main()
