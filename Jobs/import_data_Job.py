from flask_apscheduler import APScheduler
import atexit
from scripts.import_data_script import get_inspections_from_server, insert_inspections_to_db
from services.email_service import send_nouveaux_contrevenants


class ImportDataJob:
    cpt = 0

    def __init__(self):
        self.scheduler = APScheduler()

    def exec(self):
        print(f"background ask {self.cpt} running")
        inspection_from_server = get_inspections_from_server()
        contravenant = insert_inspections_to_db(inspection_from_server)
        send_nouveaux_contrevenants(contravenant)
        print(f"background task {self.cpt} finished")
        self.cpt += 1

    def start(self):
        self.scheduler.add_job(func=self.exec, trigger="cron", minute="30", hour="20", day="*", id='1')
        self.scheduler.start()
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: self.scheduler.shutdown())

