import multiprocessing
import os

msgs = ["Hi", "Hello", "How are you??", "END"]


def send_msgs(conn, msgs):
    for msg in msgs:
        conn.send(msg)
    conn.close()


def recv_msgs(conn):
    while 1:
        msg = conn.recv()
        if msg == "END":
            break
        print(msg)


sendEnd, rcvEnd = multiprocessing.Pipe()

# proc = os.fork()
#
# if proc < 0:
#     print("Fork didn't work!!")
#     exit(0)


# p1 = multiprocessing.Process(target=send_msgs, args=(sendEnd, msgs))
# p2 = multiprocessing.Process(target=recv_msgs, args=(rcvEnd,))
#
# p1.start()
# p2.start()
# p1.join()
# p2.join()



