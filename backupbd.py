import os
import sqlite3


def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')


def backup():
    SCR = f'backup/'

    if not os.path.isdir(os.path.join(os.getcwd(), SCR)):
        path = os.path.join(os.getcwd(), SCR)
        os.mkdir(path)
    con = sqlite3.connect('Dbase.db3')
    bck = sqlite3.connect(f'backup/backup.db3')
    with bck:
        con.backup(bck, pages=1, progress=progress)
    bck.close()
    con.close()