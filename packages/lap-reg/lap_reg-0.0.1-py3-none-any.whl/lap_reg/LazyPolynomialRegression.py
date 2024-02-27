import numpy as np
from .alreadyInitialized import alreadyInitialized
from .Model import Model
from .PowerDecider import PowerDecider
from .PolynomialColumnsAdder import PolynomialColumnsAdder


class LazyPolynomialRegression:

    __power_decider: PowerDecider = None
    __model: Model = None
    __polynomial_column_adder: PolynomialColumnsAdder = None


    def __init__(self, alpha: int, divisions: int, power_decider_parameter: str, model: Model) -> None:
        self.__power_decider = PowerDecider(alpha, divisions, power_decider_parameter)
        self.model = model


    def fit(self, X: np.ndarray, y: np.ndarray, *args, **kwargs) -> np.ndarray:
        powers = self.__power_decider.fit(X, y)
        self.__polynomial_column_adder = PolynomialColumnsAdder(powers)
        X_preprocessed = self.__polynomial_column_adder.transform(X)
        self.__model.fit(X_preprocessed, y, *args, **kwargs)

        return powers

    def predict(self, X: np.ndarray) -> np.ndarray:
        X_preprocessed = self.__polynomial_column_adder.transform(X)
        predictions = self.__model.predict(X_preprocessed)

        return predictions


    @property
    def power_decider(self):
        return self.__power_decider


    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        alreadyInitialized(self.__model, 'model')

        if not isinstance(model, Model):
            raise Exception('Wrong "model" value, passed model must contain "fit" and "predict" methods.')

        self.__model = model


    @property
    def polynomial_column_adder(self):
        return self.__polynomial_column_adder
