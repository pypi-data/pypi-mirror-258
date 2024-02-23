import asyncio
import aiofiles
import aiodns
import argparse
import logging
import platform
from collections.abc import Awaitable


logger = logging.getLogger("aki")


async def query(resolver: aiodns.DNSResolver,
                domain: str,
                record_type=str) -> Awaitable:
    try:
        logger.info(f"Performing {record_type} lookup on {domain}")

        return await resolver.query(domain, record_type)
    except aiodns.error.DNSError as error:
        logger.info(f"{error}")
    except Exception as error:
        logger.exception(f"{error}")


async def bruteforce(
        domain: str, wordlist: str, output: str, ipv6=False) -> None:
    resolver = aiodns.DNSResolver()

    logger.debug(f"Opening output file {output}")

    async with aiofiles.open(output, mode="w") as output_file:
        logger.debug(f"Opening wordlist file {wordlist}")

        async with aiofiles.open(wordlist, mode="r") as wordlist_file:
            logger.debug("Iterating over every line in wordlist file stream")

            async for line in wordlist_file:
                subdomain = line.strip() + "." + domain

                a_records = await query(resolver, subdomain, "A")

                if a_records is not None:
                    for record in a_records:
                        message = f"{subdomain} {record.host}"

                        logger.info(f"A record found: {message}")

                        await output_file.write(f"{message}\n")

                if ipv6:
                    aaaa_records = await query(resolver, subdomain, "AAAA")

                    if aaaa_records is not None:
                        for record in aaaa_records:
                            message = f"{subdomain} {record.host}"

                            logger.info(f"AAAA record found: {message}")

                            await output_file.write(f"{message}\n")


def main():
    parser = argparse.ArgumentParser("Aki - Asynchronous DNS Brute Forcer")

    parser.add_argument("domain", help="Root domain")
    parser.add_argument("wordlist",
                        help="Wordlist used to generate subdomains")
    parser.add_argument("output", help="Output file")
    parser.add_argument("--ipv6",
                        action="store_true",
                        help="Grab AAAA/IPv6 records")
    parser.add_argument("-v",
                        "--verbose",
                        action="count",
                        default=0,
                        help="Verbosity")

    args = parser.parse_args()

    domain = args.domain
    wordlist = args.wordlist
    output = args.output
    ipv6 = args.ipv6

    log_level = logging.ERROR

    match args.verbose:
        case 0:
            log_level = logging.ERROR
        case 1:
            log_level = logging.WARNING
        case 2:
            log_level = logging.INFO
        case 3:
            log_level = logging.DEBUG
        case 4:
            log_level = logging.CRITICAL
        case _:
            log_level = logging.DEBUG

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.setLevel(log_level)

    logger.debug("Checking OS")

    if platform.system() == "Windows":
        logger.debug("Windows OS detected, setting event loop policy")

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    logger.info(f"Peforming bruteforce attack on {domain} IPv6={ipv6}")
    logger.info(f"Using wordlist {wordlist}")
    logger.info(f"Saving output to {output}")

    asyncio.run(bruteforce(domain, wordlist, output, ipv6))


if __name__ == "__main__":
    main()
