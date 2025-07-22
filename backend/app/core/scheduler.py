import threading
import time
from app.scrapers.drhorton_elevon import DRHortonElevonScraper
from app.db.session import SessionLocal
from app.services.change_detection import detect_and_update_changes

SCRAPE_INTERVAL_SECONDS = 15 * 60  # 15 minutes

class ScraperScheduler:
    def __init__(self):
        self.scraper = DRHortonElevonScraper()
        self.timer = None
        self.running = False

    def start(self):
        self.running = True
        self.schedule_next_run()

    def stop(self):
        self.running = False
        if self.timer:
            self.timer.cancel()

    def schedule_next_run(self):
        if self.running:
            self.timer = threading.Timer(SCRAPE_INTERVAL_SECONDS, self.run)
            self.timer.start()

    def run(self):
        print("[Scheduler] Running scraper...")
        db = SessionLocal()
        try:
            plans = self.scraper.fetch_plans()
            if plans:
                detect_and_update_changes(db, plans)
                print(f"[Scheduler] Updated {len(plans)} plans.")
            else:
                print("[Scheduler] No plans found or scraping failed.")
        except Exception as e:
            print(f"[Scheduler] Error: {e}")
        finally:
            db.close()
        self.schedule_next_run()

scheduler = ScraperScheduler() 