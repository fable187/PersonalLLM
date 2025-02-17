from dataclasses import dataclass, field

@dataclass
class GCPSecret:
    KEY_LOCATION: str = field(default=None)

@dataclass
class KrakenReadOnlySecret(GCPSecret):    
    KEY_LOCATION: str = field(default="projects/trading-app-project-450322/secrets/KRAKEN_PUB_KEY_READONLY/versions/latest")
