"""Tests for Look and Feel Assessor module"""

import unittest
import numpy as np
from clar.ai.look_feel_assessor import LookFeelAssessor


class TestLookFeelAssessor(unittest.TestCase):
    """Test cases for LookFeelAssessor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.assessor = LookFeelAssessor()
        
    def test_initialization(self):
        """Test assessor initialization"""
        self.assertIsNotNone(self.assessor.style_database)
        self.assertIn('casual', self.assessor.style_database)
        
    def test_assess_visual_appeal(self):
        """Test visual appeal assessment"""
        # Create a sample image
        image = np.random.randint(0, 256, (600, 400, 3), dtype=np.uint8)
        
        assessment = self.assessor.assess_visual_appeal(image)
        
        self.assertIn('overall_appeal', assessment)
        self.assertIn('color_harmony', assessment)
        self.assertIn('rating', assessment)
        self.assertGreaterEqual(assessment['overall_appeal'], 0)
        self.assertLessEqual(assessment['overall_appeal'], 100)
        
    def test_analyze_style_match(self):
        """Test style matching analysis"""
        design_features = {'cut': 'relaxed', 'fit': 'comfortable'}
        
        match = self.assessor.analyze_style_match(design_features, 'casual')
        
        self.assertIn('match_score', match)
        self.assertIn('target_style', match)
        self.assertEqual(match['target_style'], 'casual')
        
    def test_analyze_invalid_style(self):
        """Test analyzing with invalid style"""
        design_features = {}
        
        with self.assertRaises(ValueError):
            self.assessor.analyze_style_match(design_features, 'invalid_style')
            
    def test_predict_material_feel(self):
        """Test material feel prediction"""
        feel = self.assessor.predict_material_feel('cotton')
        
        self.assertIn('softness', feel)
        self.assertIn('breathability', feel)
        self.assertIn('texture', feel)
        self.assertEqual(feel['softness'], 80)
        
    def test_predict_unknown_material_feel(self):
        """Test predicting feel for unknown material"""
        feel = self.assessor.predict_material_feel('unknown_material')
        
        # Should return default values
        self.assertEqual(feel['softness'], 50)
        
    def test_generate_aesthetic_report(self):
        """Test generating aesthetic report"""
        garment_data = {
            'image': np.random.randint(0, 256, (600, 400, 3), dtype=np.uint8),
            'material': 'silk'
        }
        
        report = self.assessor.generate_aesthetic_report(garment_data)
        
        self.assertIsInstance(report, str)
        self.assertIn('Aesthetic Assessment Report', report)
        self.assertIn('Material Feel Prediction', report)


if __name__ == '__main__':
    unittest.main()
