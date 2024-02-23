import asyncio
import aiodns
import platform

os = platform.system()

if os == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def google_a_record_lookup() -> bool:
    resolver = aiodns.DNSResolver()

    try:
        makima.record_lookup(resolver, "google.com", "A")

        return True
    except Exception:
        return False


def test_record_lookup() -> bool:
    assert google_a_record_lookup
