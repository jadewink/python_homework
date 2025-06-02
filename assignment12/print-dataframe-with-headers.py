import pandas as pd

class DFPlus(pd.DataFrame):
    @property
    def _constructor(self):
        return DFPlus

    @classmethod
    def from_csv(cls, filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)
        return cls(df)
    
    def print_with_headers(self):
        for start in range(0, len(self), 10):
            end = start + 10
            print(self.iloc[start:end])
            print()

# Create a DFPlus object from CSV
dfp = DFPlus.from_csv("../csv/products.csv")
dfp.print_with_headers()