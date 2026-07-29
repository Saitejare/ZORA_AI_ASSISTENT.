from .service import LLMService


def main():

    zora = LLMService()

    print("===== ZORA =====")
    print("Type 'exit' to quit.\n")

    while True:

        user = input("You : ")

        if user.lower() == "exit":
            break

        response = zora.chat(user)

        print(f"ZORA : {response}\n")


if __name__ == "__main__":
    main()