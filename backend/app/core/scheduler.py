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
from app.scrapers.now.cambridge.coventry import CoventryCambridgeNowScraper
from app.scrapers.now.cambridge.highlandhomes import HighlandHomesCambridgeNowScraper
from app.scrapers.now.cambridge.amlegendhomes import AmericanLegendHomesCambridgeNowScraper
from app.scrapers.now.cambridge.trophysignature import TrophySignatureCambridgeNowScraper
from app.scrapers.now.cambridge.brightlandhomes import BrightlandHomesCambridgeNowScraper
from app.scrapers.now.milrany.unionmain import UnionMainMilranyNowScraper
from app.scrapers.now.milrany.bloomfield import BloomfieldMilranyNowScraper
from app.scrapers.now.milrany.pacesetter import PacesetterMilranyNowScraper
from app.scrapers.plans.milrany.unionmain import UnionMainMilranyPlanScraper
from app.scrapers.plans.milrany.pacesetter import PacesetterMilranyPlanScraper
from app.scrapers.plans.cambridge.unionmain import UnionMainCambridgePlanScraper
from app.scrapers.plans.cambridge.coventry import CoventryCambridgePlanScraper
from app.scrapers.plans.cambridge.highlandhomes import HighlandHomesCambridgePlanScraper
from app.scrapers.plans.cambridge.amlegendhomes import AmericanLegendHomesCambridgePlanScraper
from app.scrapers.plans.cambridge.brightlandhomes import BrightlandHomesCambridgePlanScraper
from app.scrapers.now.brookville.beazerhomes import BeazerHomesBrookvilleNowScraper
from app.scrapers.now.brookville.trophysignature import TrophySignatureBrookvilleNowScraper
from app.scrapers.now.brookville.highlandhomes import HighlandHomesBrookvilleNowScraper
from app.scrapers.now.brookville.unionmain import UnionMainBrookvilleNowScraper
from app.scrapers.now.brookville.perryhomes import PerryHomesBrookvilleNowScraper
from app.scrapers.now.brookville.historymaker import HistoryMakerBrookvilleNowScraper
from app.scrapers.now.brookville.ashtonwoods import AshtonWoodsBrookvilleNowScraper
from app.scrapers.now.brookville.shaddockhomes import ShaddockHomesBrookvilleNowScraper
from app.scrapers.now.edgewater.unionmain import UnionMainEdgewaterNowScraper
from app.scrapers.now.edgewater.perryhomes import PerryHomesEdgewaterNowScraper
from app.scrapers.now.edgewater.coventryhomes import CoventryHomesEdgewaterNowScraper
from app.scrapers.now.edgewater.chesmarhomes import ChesmarHomesEdgewaterNowScraper
from app.scrapers.plans.edgewater.unionmain import UnionMainEdgewaterPlanScraper
from app.scrapers.plans.edgewater.coventryhomes import CoventryHomesEdgewaterPlanScraper
from app.scrapers.now.creekside.unionmainhomes import UnionMainHomesCreeksideNowScraper
from app.scrapers.now.creekside.highlandhomes import HighlandHomesCreeksideNowScraper
from app.scrapers.now.creekside.davidweekleyhomes import DavidWeekleyHomesCreeksideNowScraper
from app.scrapers.now.creekside.williamryanhomes import WilliamRyanHomesCreeksideNowScraper
from app.scrapers.now.creekside.rockwellhomes import RockwellHomesCreeksideNowScraper
from app.scrapers.plans.brookville.beazerhomes import BeazerHomesBrookvillePlanScraper
from app.scrapers.plans.creekside.unionmainhomes import UnionMainHomesCreeksidePlanScraper
from app.scrapers.plans.creekside.highlandhomes import HighlandHomesCreeksidePlanScraper
from app.scrapers.plans.creekside.davidweekleyhomes import DavidWeekleyHomesCreeksidePlanScraper
from app.scrapers.plans.creekside.williamryanhomes import WilliamRyanHomesCreeksidePlanScraper
from app.scrapers.plans.creekside.rockwellhomes import RockwellHomesCreeksidePlanScraper
from app.scrapers.plans.brookville.highlandhomes import HighlandHomesBrookvillePlanScraper
from app.scrapers.plans.brookville.unionmain import UnionMainBrookvillePlanScraper
from app.scrapers.plans.brookville.perryhomes import PerryHomesBrookvillePlanScraper
from app.scrapers.plans.brookville.historymaker import HistoryMakerBrookvillePlanScraper
from app.scrapers.plans.brookville.ashtonwoods import AshtonWoodsBrookvillePlanScraper
from app.scrapers.plans.brookville.shaddockhomes import ShaddockHomesBrookvillePlanScraper
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
            CoventryCambridgeNowScraper(),
            HighlandHomesCambridgeNowScraper(),
            AmericanLegendHomesCambridgeNowScraper(),
            TrophySignatureCambridgeNowScraper(),
            BrightlandHomesCambridgeNowScraper(),
            UnionMainMilranyNowScraper(),
            BloomfieldMilranyNowScraper(),
            PacesetterMilranyNowScraper(),
            UnionMainMilranyPlanScraper(),
            PacesetterMilranyPlanScraper(),
            UnionMainCambridgePlanScraper(),
            CoventryCambridgePlanScraper(),
            HighlandHomesCambridgePlanScraper(),
            AmericanLegendHomesCambridgePlanScraper(),
            BrightlandHomesCambridgePlanScraper(),
            BeazerHomesBrookvilleNowScraper(),
            TrophySignatureBrookvilleNowScraper(),
            HighlandHomesBrookvilleNowScraper(),
            UnionMainBrookvilleNowScraper(),
            PerryHomesBrookvilleNowScraper(),
            HistoryMakerBrookvilleNowScraper(),
            AshtonWoodsBrookvilleNowScraper(),
            ShaddockHomesBrookvilleNowScraper(),
            UnionMainEdgewaterNowScraper(),
            PerryHomesEdgewaterNowScraper(),
            CoventryHomesEdgewaterNowScraper(),
            ChesmarHomesEdgewaterNowScraper(),
            UnionMainEdgewaterPlanScraper(),
            CoventryHomesEdgewaterPlanScraper(),
            UnionMainHomesCreeksideNowScraper(),
            HighlandHomesCreeksideNowScraper(),
            DavidWeekleyHomesCreeksideNowScraper(),
            WilliamRyanHomesCreeksideNowScraper(),
            RockwellHomesCreeksideNowScraper(),
            BeazerHomesBrookvillePlanScraper(),
            UnionMainHomesCreeksidePlanScraper(),
            HighlandHomesCreeksidePlanScraper(),
            DavidWeekleyHomesCreeksidePlanScraper(),
            WilliamRyanHomesCreeksidePlanScraper(),
            RockwellHomesCreeksidePlanScraper(),
            HighlandHomesBrookvillePlanScraper(),
            UnionMainBrookvillePlanScraper(),
            PerryHomesBrookvillePlanScraper(),
            HistoryMakerBrookvillePlanScraper(),
            AshtonWoodsBrookvillePlanScraper(),
            ShaddockHomesBrookvillePlanScraper(),
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