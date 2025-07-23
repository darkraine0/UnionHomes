import threading
import time
from app.scrapers.drhorton_elevon import DRHortonElevonScraper
from app.scrapers.unionmain_elevon import UnionMainElevonScraper
from app.db.session import SessionLocal
from app.services.change_detection import detect_and_update_changes

SCRAPE_INTERVAL_SECONDS = 300  # 5 minutes

class ScraperScheduler:
    def __init__(self):
        # Add all scraper instances here as you implement more
        self.scrapers = [
            DRHortonElevonScraper(),
            UnionMainElevonScraper(),
        ]
        self.timer = None
        self.running = False

    def start(self):
        self.running = True
        self.run()  # Run immediately on startup
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
        print("[Scheduler] Running all scrapers...")
        db = SessionLocal()
        try:
            for scraper in self.scrapers:
                print(f"[Scheduler] Running scraper: {scraper.__class__.__name__}")
                plans = scraper.fetch_plans()
                if plans:
                    detect_and_update_changes(db, plans)
                    print(f"[Scheduler] {scraper.__class__.__name__}: Updated {len(plans)} plans.")
                else:
                    print(f"[Scheduler] {scraper.__class__.__name__}: No plans found or scraping failed.")
        except Exception as e:
            print(f"[Scheduler] Error: {e}")
        finally:
            db.close()
        self.schedule_next_run()

scheduler = ScraperScheduler() 