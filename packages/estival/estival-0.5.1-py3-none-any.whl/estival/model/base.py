import pandas as pd
from dataclasses import dataclass


@dataclass
class ResultsData:
    derived_outputs: pd.DataFrame
    extras: dict
