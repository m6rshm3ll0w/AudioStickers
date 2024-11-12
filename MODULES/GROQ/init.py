from datetime import datetime
from groq import Groq

client = None


def groq_init(KEY):
    global client
    print(f" > INITIALISE GroqAPI ....... ", end="")
    try:
        # noinspection SpellCheckingInspection
        GroqCloudAPISECRETKEY = "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"
        client = Groq(
            api_key=GroqCloudAPISECRETKEY,
        )
        print("DONE")
    except Exception as Except_:
        print("NO\n"
              "\033[3m\033[31m{}\033[0m".format(f"[{datetime.now()}] ERROR: {Except_}"))
        exit()