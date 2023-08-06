import unittest
from unittest.mock import Mock

from ViewController.Planet import Planet


class RocketTest(unittest.TestCase):

    def setUp(self):
        self.planet = Planet(0, 0, 695 * 10 ** 6, (0, 0, 0), 1.98892 * 10 ** 30, "test", 0)
        self.rocket = Mock()
        self.rocket.currentStep = 0
        self.rocket.position_X = [100, 0, -100]
        self.rocket.position_Y = [100, 0, -100]

    def test_collision_within_radius(self):
        # Set up the scenario where there is a collision (distance <= radius * 95%)
        self.planet.distanceToRocket = self.planet.radius * 94 / 100
        self.assertTrue(self.planet.check_collision())

    def test_collision_outside_radius(self):
        # Set up the scenario where there is no collision (distance > radius * 95%)
        self.planet.distanceToRocket = self.planet.radius * 96 / 100
        self.assertFalse(self.planet.check_collision())

    def test_collision_at_exact_radius(self):
        # Set up the scenario where the distance is exactly at the 95% of the radius
        self.planet.distanceToRocket = self.planet.radius * 95 / 100
        self.assertTrue(self.planet.check_collision())

    def test_set_scale_positive(self):
        # Set up the scenario where the scale factor is positive
        initial_scale = self.planet.scaleR
        scale_factor = 2.0
        self.planet.set_scale(scale_factor)
        expected_scale = initial_scale * scale_factor
        self.assertEqual(self.planet.scaleR, expected_scale)

    def test_set_scale_zero(self):
        # Set up the scenario where the scale factor is zero
        initial_scale = self.planet.scaleR
        scale_factor = 0.0
        self.planet.set_scale(scale_factor)
        self.assertEqual(self.planet.scaleR, initial_scale)

    def test_set_scale_negative(self):
        # Set up the scenario where the scale factor is negative
        initial_scale = self.planet.scaleR
        scale_factor = -1.5
        self.planet.set_scale(scale_factor)
        self.assertEqual(self.planet.scaleR, initial_scale)


if __name__ == '__main__':
    unittest.main()
