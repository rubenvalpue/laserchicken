import unittest

import numpy as np

from laserchicken import read_las, keys
from laserchicken.feature_extractor.var_feature_extractor import VarianceFeatureExtractor
from laserchicken.test_tools import create_point_cloud


class TestVariationZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = [89664, 23893, 30638, 128795, 62052, 174453, 29129, 17127, 128215, 29667, 116156, 119157, 98591,
                        7018,
                        61494, 65194, 117931, 62971, 10474, 90322]
        var_z = self.extractor.extract(pc_in, neighborhood, None, None, None)
        np.testing.assert_allclose(var_z, 1.8408359999999995)

    def test_height_stats_without_neighbors(self):
        pc_in = read_las.read("testdata/AHN2.las")
        neighborhood = []
        var_z = self.extractor.extract(pc_in, neighborhood, pc_in, None, None)
        assert np.isnan(var_z)

    def test_default_provides_correct(self):
        feature_names = self.extractor.provides()
        self.assertIn('var_z', feature_names)

    def setUp(self):
        self.extractor = VarianceFeatureExtractor()


class TestVarianceNormZFeatureExtractor(unittest.TestCase):
    def test_height_stats(self):
        x = y = np.array([0, 0, 0])
        z = np.array([2, 2, 2])
        normalized_z = np.array([3, 4, 5])
        point_cloud = create_point_cloud(x, y, z, normalized_z=normalized_z)
        neighborhood = [[0, 1, 2]]

        variance = self.extractor.extract(point_cloud, neighborhood, None, None, None)

        self.assertAlmostEquals(variance, 2 / 3)

    def test_default_provides_correct(self):
        feature_names = self.extractor.provides()
        self.assertIn('var_normalized_height', feature_names)

    def setUp(self):
        self.extractor = VarianceFeatureExtractor(data_key=keys.normalized_height)