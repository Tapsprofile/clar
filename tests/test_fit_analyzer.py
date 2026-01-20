"""Tests for AI Fit Analyzer module"""

import unittest
import numpy as np
from clar.ai.fit_analyzer import FitAnalyzer


class TestFitAnalyzer(unittest.TestCase):
    """Test cases for FitAnalyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = FitAnalyzer()
        
    def test_initialization(self):
        """Test fit analyzer initialization"""
        self.assertIsNotNone(self.analyzer.fit_model)
        self.assertEqual(len(self.analyzer.body_measurements), 0)
        
    def test_set_body_measurements(self):
        """Test setting body measurements"""
        measurements = {
            'chest': 95,
            'waist': 80,
            'hips': 98,
            'shoulder_width': 45,
            'arm_length': 60
        }
        
        self.analyzer.set_body_measurements(measurements)
        self.assertEqual(self.analyzer.body_measurements, measurements)
        
    def test_set_body_measurements_missing_keys(self):
        """Test setting incomplete body measurements"""
        measurements = {
            'chest': 95,
            'waist': 80
        }
        
        with self.assertRaises(ValueError):
            self.analyzer.set_body_measurements(measurements)
            
    def test_analyze_fit(self):
        """Test fit analysis"""
        body = {
            'chest': 95,
            'waist': 80,
            'hips': 98,
            'shoulder_width': 45,
            'arm_length': 60
        }
        garment = {
            'chest': 100,
            'waist': 85,
            'hips': 102
        }
        
        self.analyzer.set_body_measurements(body)
        self.analyzer.set_garment_measurements(garment)
        
        results = self.analyzer.analyze_fit()
        
        self.assertIn('overall_fit_score', results)
        self.assertIn('areas', results)
        self.assertIn('recommendations', results)
        self.assertGreater(results['overall_fit_score'], 0)
        
    def test_analyze_fit_without_measurements(self):
        """Test fit analysis without measurements should raise error"""
        with self.assertRaises(ValueError):
            self.analyzer.analyze_fit()
            
    def test_suggest_size(self):
        """Test size suggestion"""
        measurements = {
            'chest': 92,
            'waist': 78,
            'hips': 95,
            'shoulder_width': 44,
            'arm_length': 58
        }
        
        self.analyzer.set_body_measurements(measurements)
        size = self.analyzer.suggest_size()
        
        self.assertEqual(size, 'S')
        
    def test_detect_pressure_points(self):
        """Test pressure point detection"""
        body_scan = np.random.rand(100, 3)
        garment_mesh = np.random.rand(100, 3)
        
        pressure_points = self.analyzer.detect_pressure_points(body_scan, garment_mesh)
        
        self.assertIsInstance(pressure_points, list)


if __name__ == '__main__':
    unittest.main()
