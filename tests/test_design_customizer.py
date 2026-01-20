"""Tests for Design Customizer module"""

import unittest
from clar.design.customizer import DesignCustomizer


class TestDesignCustomizer(unittest.TestCase):
    """Test cases for DesignCustomizer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.customizer = DesignCustomizer()
        
    def test_initialization(self):
        """Test customizer initialization"""
        self.assertIsNotNone(self.customizer.available_patterns)
        self.assertIsNotNone(self.customizer.color_palettes)
        self.assertEqual(len(self.customizer.design_history), 0)
        
    def test_create_new_design(self):
        """Test creating a new design"""
        design = self.customizer.create_new_design('tshirt')
        
        self.assertEqual(design['template'], 'tshirt')
        self.assertIn('colors', design)
        self.assertIn('pattern', design)
        self.assertEqual(len(self.customizer.design_history), 1)
        
    def test_change_color(self):
        """Test changing design color"""
        self.customizer.create_new_design('tshirt')
        self.customizer.change_color('primary', (255, 0, 0))
        
        self.assertEqual(self.customizer.current_design['colors']['primary'], (255, 0, 0))
        
    def test_apply_pattern(self):
        """Test applying a pattern"""
        self.customizer.create_new_design('tshirt')
        self.customizer.apply_pattern('stripes', {'width': 5})
        
        self.assertEqual(self.customizer.current_design['pattern'], 'stripes')
        
    def test_apply_invalid_pattern(self):
        """Test applying an invalid pattern"""
        self.customizer.create_new_design('tshirt')
        
        with self.assertRaises(ValueError):
            self.customizer.apply_pattern('invalid_pattern')
            
    def test_adjust_dimensions(self):
        """Test adjusting dimensions"""
        self.customizer.create_new_design('tshirt')
        self.customizer.adjust_dimensions('length', 75)
        
        self.assertEqual(self.customizer.current_design['dimensions']['length'], 75)
        
    def test_add_embellishment(self):
        """Test adding embellishment"""
        self.customizer.create_new_design('tshirt')
        self.customizer.add_embellishment('pocket', (0.2, 0.5), size=1.2)
        
        self.assertEqual(len(self.customizer.current_design['embellishments']), 1)
        
    def test_apply_color_palette(self):
        """Test applying color palette"""
        self.customizer.create_new_design('tshirt')
        self.customizer.apply_color_palette('ocean')
        
        # Ocean palette should have at least 2 colors
        self.assertIsNotNone(self.customizer.current_design['colors']['primary'])
        self.assertIsNotNone(self.customizer.current_design['colors']['secondary'])
        
    def test_undo_modification(self):
        """Test undoing modifications"""
        self.customizer.create_new_design('tshirt')
        self.customizer.change_color('primary', (255, 0, 0))
        
        modifications_before = len(self.customizer.current_design['modifications'])
        result = self.customizer.undo_last_modification()
        
        self.assertTrue(result)
        self.assertLess(len(self.customizer.current_design['modifications']), modifications_before)
        
    def test_get_design_summary(self):
        """Test getting design summary"""
        self.customizer.create_new_design('tshirt')
        self.customizer.apply_pattern('stripes')
        
        summary = self.customizer.get_design_summary()
        
        self.assertIn('template', summary)
        self.assertIn('modifications_count', summary)
        
    def test_export_design(self):
        """Test exporting design"""
        self.customizer.create_new_design('tshirt')
        exported = self.customizer.export_design()
        
        self.assertEqual(exported['template'], 'tshirt')
        
    def test_generate_variations(self):
        """Test generating design variations"""
        self.customizer.create_new_design('tshirt')
        variations = self.customizer.generate_variations(count=3)
        
        self.assertEqual(len(variations), 3)


if __name__ == '__main__':
    unittest.main()
