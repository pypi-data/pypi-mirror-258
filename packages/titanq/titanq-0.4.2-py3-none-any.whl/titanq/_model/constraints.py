
import numpy as np


class Constraints:
    """
    Constraints passed to TitanQ platform. It is consisted of the weights_constraints matrix and the bias_constraints vector.
    """

    def __init__(self, variable_size: int, weights: np.ndarray, bias: np.ndarray) -> None:
        """
        :raise ValueError:
        """
        bias_shape = bias.shape
        weights_shape = weights.shape

        # validate shapes
        if len(weights_shape) != 2:
            raise ValueError(f"Weights constraints should be a 2d matrix. Got something with shape: {weights_shape}")

        if len(bias_shape) != 1:
            raise ValueError(f"Bias constraints should be a vector. Got something with shape: {bias_shape}")

        if weights_shape[1] != variable_size:
            raise ValueError(f"Weights constraints shape does not match variable size. Expected (M, {variable_size}) where M is the number of constraints")
        n_constraints = weights_shape[0]

        if n_constraints == 0:
            raise ValueError("Need at least 1 constraints")

        if bias_shape[0] != n_constraints:
            raise ValueError(f"Bias constraints shape does not match weights constraints size. Expected ({n_constraints}, )")


        # validate dtype
        if weights.dtype != np.float32:
            raise ValueError(f"Weights constraints vector dtype should be np.float32")

        if bias.dtype != np.float32:
            raise ValueError(f"Bias constraints vector dtype should be np.float32")

        self._bias = bias
        self._weights = weights

    def bias(self) -> np.ndarray:
        """
        :return: The bias vector of this constraint.
        """
        return self._bias

    def weights(self) -> np.ndarray:
        """
        :return: The weights matrix of this constraint.
        """
        return self._weights