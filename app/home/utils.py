import pandas as pd
import numpy as np

from sklearn.base import TransformerMixin


class UploadFile:
    def __init__(self, name, type=None, size=None, not_allowed_msg=None):
        self.name = name
        self.type = type
        self.size = size
        self.not_allowed_msg = not_allowed_msg
        self.url = "data/%s" % name
        self.delete_url = "delete/%s" % name
        self.delete_type = "DELETE"
        self.analyze_url = "analyze/%s" % name

    def get_file(self):

        if self.not_allowed_msg is not None:
            return {
                "error": self.not_allowed_msg,
                "name": self.name,
                "type": self.type,
                "size": self.size
            }

        result = {
            "name": self.name,
            "size": self.size,
            "url": self.url,
            "deleteUrl": self.delete_url,
            "deleteType": self.delete_type,
            "analyzeUrl": self.analyze_url
        }
        if self.type is not None:
            result["type"] = self.type

        return result


class DataFrameImputer(TransformerMixin):

    def __init__(self):
        pass

    def fit(self, X, y=None):

        self.fill = pd.Series([
            X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
            index=X.columns
        )

        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)
