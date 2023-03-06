from typing import Any, Optional

import pandas as pd
from fold.models.base import Model


class UnivariateStatsForecast(Model):

    properties = Model.Properties(
        requires_continuous_updates=True,
        model_type=Model.Properties.ModelType.regressor,
    )

    name = "UnivariateStatsForecast"
    fitted = False

    def __init__(self, model: Any) -> None:
        self.model = model
        self.name = "UnivariateStatsForecast-{model.alias}"

    def fit(
        self, X: pd.DataFrame, y: pd.Series, sample_weights: Optional[pd.Series] = None
    ) -> None:
        if self.fitted:
            if hasattr(self.model, "update"):
                self.model.update(y=y.values)
            else:
                self.model.fit(y=y.values)
        else:
            self.model.fit(y=y.values)
            self.fitted = True

    # TODO: figure out whether we'll want to support in-sample predictions, and whether the Model
    # should be responsible for handling that or the "loop".
    # def predict_in_sample(self, X: np.ndarray) -> np.ndarray:
    #     pred_dict = self.model.predict_in_sample()
    #     if "fitted" in pred_dict:
    #         return pred_dict["fitted"]
    #     elif "mean" in pred_dict:
    #         return pred_dict["mean"]
    #     else:
    #         raise ValueError("Unknown prediction dictionary structure")

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        return pd.Series(self.model.predict(h=len(X))["mean"], index=X.index)