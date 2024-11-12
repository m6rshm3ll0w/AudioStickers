from datetime import datetime

from MODULES.IMGs import TEXT2IMG


def fusion_init(KEY, SECRET):
    print(f" > INIT. FUSION BRAIN API ... ", end="")
    try:
        # noinspection SpellCheckingInspection
        TEXT2IMG.INITIAL_API(KEY, SECRET)
        print("DONE")
    except Exception as Except_:
        print("NO\n"
              "\033[3m\033[31m{}\033[0m".format(f"[{datetime.now()}] ERROR: {Except_}"))
        exit()