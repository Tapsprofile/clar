"""Tests for VR Interface module"""

import unittest
import numpy as np
from clar.vr.interface import VRInterface


class TestVRInterface(unittest.TestCase):
    """Test cases for VRInterface"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.vr = VRInterface(resolution=(1920, 1080))
        
    def test_initialization(self):
        """Test VR interface initialization"""
        self.assertEqual(self.vr.resolution, (1920, 1080))
        self.assertEqual(len(self.vr.garments), 0)
        self.assertFalse(self.vr.vr_enabled)
        
    def test_initialize_vr_environment(self):
        """Test VR environment initialization"""
        result = self.vr.initialize_vr_environment()
        self.assertTrue(result)
        self.assertTrue(self.vr.vr_enabled)
        self.assertIsNotNone(self.vr.current_scene)
        
    def test_load_garment_model(self):
        """Test loading a garment model"""
        self.vr.initialize_vr_environment()
        
        garment_data = {
            'mesh': np.random.rand(10, 3),
            'texture': None,
            'material': 'cotton'
        }
        
        result = self.vr.load_garment_model(garment_data)
        self.assertTrue(result)
        self.assertEqual(len(self.vr.garments), 1)
        
    def test_load_garment_without_init(self):
        """Test loading garment without VR initialization should raise error"""
        garment_data = {'mesh': [], 'texture': None}
        
        with self.assertRaises(RuntimeError):
            self.vr.load_garment_model(garment_data)
            
    def test_render_scene(self):
        """Test scene rendering"""
        self.vr.initialize_vr_environment()
        scene = self.vr.render_scene()
        
        self.assertIsInstance(scene, np.ndarray)
        self.assertEqual(scene.shape, (1080, 1920, 3))
        
    def test_apply_physics(self):
        """Test physics application"""
        self.vr.initialize_vr_environment()
        garment_data = {'mesh': [], 'texture': None}
        self.vr.load_garment_model(garment_data)
        
        self.vr.apply_physics(gravity=9.8, wind=(0.5, 0, 0))
        
        self.assertIn('physics_state', self.vr.garments[0])
        self.assertEqual(self.vr.garments[0]['physics_state']['gravity'], 9.8)
        
    def test_get_garment_info(self):
        """Test retrieving garment information"""
        self.vr.initialize_vr_environment()
        garment_data = {'mesh': [], 'texture': None, 'material': 'silk'}
        self.vr.load_garment_model(garment_data)
        
        info = self.vr.get_garment_info(0)
        self.assertIsNotNone(info)
        self.assertEqual(info['material'], 'silk')
        
        # Test invalid ID
        invalid_info = self.vr.get_garment_info(999)
        self.assertIsNone(invalid_info)
        
    def test_set_camera_position(self):
        """Test camera positioning"""
        self.vr.initialize_vr_environment()
        self.vr.set_camera_position((1, 2, 3), (10, 20, 30))
        
        self.assertEqual(self.vr.current_scene['camera_position'], [1, 2, 3])
        self.assertEqual(self.vr.current_scene['camera_rotation'], [10, 20, 30])


if __name__ == '__main__':
    unittest.main()
