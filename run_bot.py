from multiprocessing import Lock, Process, Queue, current_process
from bot import LongreadBot


if __name__ == "__main__":

    tasks_to_do = Queue()

    bot = LongreadBot(tasks_to_do)
    render_p = Process(target=LongreadBot.render, args=(bot, tasks_to_do))
    render_p.start()

    bot_p = Process(target=LongreadBot.main, args=(bot,))
    bot_p.start()

    render_p.join()
    bot_p.join()
