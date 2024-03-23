from db.models import Symbols, Klines


class ByBitTables:
    PerpDaily = Symbols.BBPerpetualSymbolsDaily
    SpotDaily = Symbols.BBSpotSymbolsDaily

    Perp = Symbols.BBPerpetualSymbols
    Spot = Symbols.BBSpotSymbols

    PerpSchedule = Klines.ByBitPerpetualKlineDownloadSchedule


class Tags:
    upload = {
        "name": "Upload",
        "description": "Operations related to uploading data",
    }
    process = {
        "name": "Process",
        "description": "Operations related to processing raw data",
    }
    markets = {
        "name": "Markets",
        "description": "Operations related to symbol markets",
    }


tags_metadata = [Tags.upload, Tags.process, Tags.markets]
