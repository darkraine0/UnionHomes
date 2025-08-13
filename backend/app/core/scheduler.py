import threading
import time
from app.scrapers.now.elevon.drhorton import DRHortonElevonNowScraper
from app.scrapers.now.elevon.unionmain import UnionMainElevonNowScraper
from app.scrapers.now.elevon.historymaker import HistoryMakerElevonNowScraper
from app.scrapers.now.elevon.mihomes import MIHomesElevonNowScraper
from app.scrapers.now.elevon.trophysignature import TrophySignatureElevonNowScraper
from app.scrapers.now.elevon.pacesetter import PacesetterElevonNowScraper
from app.scrapers.now.elevon.khovnanian import KHovnanianElevonNowScraper
from app.scrapers.plans.elevon.drhorton import DRHortonElevonPlanScraper
from app.scrapers.plans.elevon.unionmain import UnionMainElevonPlanScraper
from app.scrapers.plans.elevon.historymaker import HistoryMakerElevonPlanScraper
from app.scrapers.plans.elevon.khovnanian import KHovnanianElevonPlanScraper
from app.scrapers.plans.elevon.mihomes import MIHomesElevonPlanScraper
from app.scrapers.plans.elevon.pacesetter import PacesetterElevonPlanScraper
from app.scrapers.plans.elevon.trophysignature import TrophySignatureElevonPlanScraper
from app.scrapers.now.cambridge.unionmain import UnionMainCambridgeNowScraper
from app.scrapers.plans.cambridge.unionmain import UnionMainCambridgePlanScraper
from app.db.session import SessionLocal
from app.services.change_detection import detect_and_update_changes

SCRAPE_INTERVAL_SECONDS = 300  # 5 minutes

class ScraperScheduler:
    def __init__(self):
        # Add all scraper instances here as you implement more
        self.scrapers = [
            DRHortonElevonNowScraper(),
            UnionMainElevonNowScraper(),
            HistoryMakerElevonNowScraper(),
            MIHomesElevonNowScraper(),
            TrophySignatureElevonNowScraper(),
            PacesetterElevonNowScraper(),
            KHovnanianElevonNowScraper(),
            DRHortonElevonPlanScraper(),
            UnionMainElevonPlanScraper(),
            HistoryMakerElevonPlanScraper(),
            KHovnanianElevonPlanScraper(),
            MIHomesElevonPlanScraper(),
            PacesetterElevonPlanScraper(),
            TrophySignatureElevonPlanScraper(),
            UnionMainCambridgeNowScraper(),
            UnionMainCambridgePlanScraper(),
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