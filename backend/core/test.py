from backend.core.capability_registry import CapabilityRegistry


def test():

    registry = CapabilityRegistry()

    print("=" * 60)

    print(
        registry.list_capabilities()
    )

    print("=" * 60)

    print(
        registry.execute(
            "application",
            "launch",
            {
                "target": "chrome"
            }
        )
    )

    print("=" * 60)

    print(
        registry.execute(
            "browser",
            "open_url",
            {
                "url": "github.com"
            }
        )
    )

    input("\nPress Enter...")

    registry.execute(
        "browser",
        "close",
        {}
    )


if __name__ == "__main__":

    try:

        test()

        print("\n✅ Capability Registry Passed")

    except Exception as e:

        print("\n❌ Capability Registry Failed")

        print(type(e).__name__)

        print(e)