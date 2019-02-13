import unittest

import numpy as np

from laserchicken import read_las
from laserchicken.feature_extractor.mean_std_coeff_z_feature_extractor import MeanStdCoeffZFeatureExtractor


class TestMeanZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = [89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591,
                        7018,
                        61494, 65194, 117931, 62971, 10474, 90322]
        mean_z, std_z, coeff_var_z = MeanStdCoeffZFeatureExtractor().extract(pc_in, neighborhood, None, None, None)
        np.testing.assert_allclose(mean_z, 1.3779999737739566)
        np.testing.assert_allclose(std_z, 1.3567741153191268)
        np.testing.assert_allclose(coeff_var_z, 0.9845966191155302)

    def test_height_stats_without_neighbors(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = []
        mean_z, std_z, coeff_var_z = MeanStdCoeffZFeatureExtractor().extract(pc_in, neighborhood, pc_in, None, None)
        assert np.isnan(mean_z)
        assert np.isnan(std_z)
        assert np.isnan(coeff_var_z)