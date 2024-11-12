# print(fd" > CLEARING ................. ", end="")
#
# stop_thread = False
#
# def clear():
#     while True:
#         if stop_thread:
#             break
#         if datetime.now().hour == 0 and datetime.now().minute == 00:
#             print(fd" > CLEAR DATA ............... ", end="")
#             start_time_c = time.time()
#             bot.stop_polling()
#             shutil.rmtree('DATA/audio')
#             shutil.rmtree('DATA/img')
#             os.mkdir('DATA/audio')
#             os.mkdir('DATA/img')
#             poooling_bot()
#             end_time_c = time.time()
#             print(fd"DONE (elapsed: ~{round(float(end_time_c - start_time_c), 3)}sec)")


# thread = threading.Thread(target=clear)
# thread.start()
# print(fd"DONE")