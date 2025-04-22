from dataclasses import dataclass, field

@dataclass
class GCPSecret:
    KEY_LOCATION: str = field(default=None)
    NAME: str = field(default=None)
    VALUE: str = field(default=None)


@dataclass
class GCPSecretSamples(GCPSecret):
    KEY_LOCATION: str = field(default="projects/308569288477/secrets/SampleSecret/versions/1")
    NAME: str = field(default="SampleSecret")
    VALUE: str = field(default="SampleValue")

@dataclass
class KrakenReadOnlySecret(GCPSecret):    
    KEY_LOCATION: str = field(default="projects/trading-app-project-450322/secrets/KRAKEN_PUB_KEY_READONLY/versions/latest")


@dataclass
class CloudRunServiceUrl:
    kraken_to_bigquery: str = field(default="https://us-central1-trading-app-project-450322.cloudfunctions.net/kraken_to_bigquery")