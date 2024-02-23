from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal

from statkit.model_selection import (
    holdout_split,
    _as_categories,
    _as_multinomial,
    _single_multinomial_train_test_split,
)


class TestHoldOutSplit(TestCase):
    def setUp(self):
        self.random_state = np.random.RandomState(42)

    def test_as_mulitnomial_and_categories(self):
        """Test that multinomial and categorical representations are inverse."""
        n_features = 10
        x_sample = self.random_state.randint(0, high=10, size=[n_features])
        x_draws = _as_categories(x_sample)
        x_test = _as_multinomial(x_draws, n_features=n_features)
        assert_array_equal(x_sample, x_test)

    def test_single_train_test_split(self):
        """Test train-test split of a single multinomial."""
        fraction = 1 / 6
        x_sample = self.random_state.randint(0, high=10, size=[10])
        x_train, x_test = _single_multinomial_train_test_split(
            self.random_state, x_sample, test_size=fraction
        )
        self.assertEqual(x_test.sum(), int(x_sample.sum() * fraction))
        self.assertEqual(x_train.sum() + x_test.sum(), x_sample.sum())
        assert_array_equal(x_train + x_test, x_sample)

    def test_holdout_split(self):
        """Test train-test split of a dataset of multinomials."""
        fraction = 1 / 3
        n_features = 10
        n_samples = 20
        x_sample = self.random_state.randint(0, high=10, size=[n_samples, n_features])
        # Triple number of observations to take out a third (=fraction).
        x_sample = x_sample * 3
        x_train, x_test = holdout_split(x_sample, test_size=fraction, random_state=43)
        self.assertEqual(x_test.sum(), int(x_sample.sum() * fraction))
        assert_array_equal(x_test.sum(axis=1), x_sample.sum(axis=1) * fraction)
        self.assertEqual(x_train.sum() + x_test.sum(), x_sample.sum())
        assert_array_equal(
            x_train.sum(axis=1) + x_test.sum(axis=1), x_sample.sum(axis=1)
        )
        assert_array_equal(x_train + x_test, x_sample)

        # Check if the function is deterministic.
        x_train2, x_test2 = holdout_split(x_sample, test_size=fraction, random_state=43)
        assert_array_equal(x_train, x_train2)
        assert_array_equal(x_test, x_test2)
