from flask_apscheduler import APScheduler
import atexit
from scripts.import_data_script import get_contrevenants_from_server, insert_contrevenants_to_db


class ImportDataJob:
    cpt = 0

    def __init__(self):
        self.scheduler = APScheduler()

    def exec(self):
        print(f"background ask {self.cpt} running")
        contrevenants_from_server = get_contrevenants_from_server()
        insert_contrevenants_to_db(contrevenants_from_server)
        print(f"background task {self.cpt} finished")
        self.cpt+=1

    def start(self):
        self.scheduler.add_job(func=self.exec, trigger="cron", minute="30", hour="20", day="*", id='1')
        self.scheduler.start()
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: self.scheduler.shutdown())

    def stop(self):
        self.scheduler.shutdown()
