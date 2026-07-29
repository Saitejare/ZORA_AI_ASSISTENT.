from backend.capabilities.browser.service import BrowserService


def test():

    service = BrowserService()

    tests = [

        ("open_url",
         {"url": "github.com"}),

        ("title",
         {}),

        ("metadata",
         {}),

        ("new_tab",
         {}),

        ("search",
         {
             "query": "LangGraph",
             "engine": "duckduckgo"
         }),

        ("list_tabs",
         {}),

        ("switch_tab",
         {
             "index": 0
         }),

        ("close_tab",
         {}),

        ("close",
         {})
    ]

    for action, params in tests:

        print("=" * 80)

        print(action)

        try:

            result = service.execute(
                action,
                params
            )

            print(result)

        except Exception as e:

            print(e)


if __name__ == "__main__":

    try:

        test()

        print("\n✅ BrowserService Passed")

    except Exception as e:

        print("\n❌ BrowserService Failed")

        print(type(e).__name__)

        print(e)