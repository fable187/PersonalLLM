from dataclasses import dataclass, field

@dataclass
class GCPSecret:
    KEY_LOCATION: str = field(default=None)


@dataclass
class KrakenReadOnlySecret(GCPSecret):    
    KEY_LOCATION: str = field(default="projects/trading-app-project-450322/secrets/KRAKEN_PUB_KEY_READONLY/versions/latest")


@dataclass
class CloudRunServiceUrl:
    kraken_to_bigquery: str = field(default="https://us-central1-trading-app-project-450322.cloudfunctions.net/kraken_to_bigquery")