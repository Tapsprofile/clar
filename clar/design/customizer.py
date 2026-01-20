"""Design customization tools for clothing"""

from typing import Dict, List, Tuple, Optional
import numpy as np


class DesignCustomizer:
    """
    Tools for customizing clothing designs including colors, patterns, and styles.
    
    Provides interactive design modification capabilities for VR-based design tools.
    """
    
    def __init__(self):
        """Initialize the Design Customizer"""
        self.current_design = {}
        self.design_history = []
        self.available_patterns = self._load_patterns()
        self.color_palettes = self._load_color_palettes()
        
    def _load_patterns(self) -> Dict:
        """Load available patterns"""
        return {
            'solid': {'type': 'solid', 'complexity': 1},
            'stripes': {'type': 'lines', 'complexity': 2, 'orientation': 'vertical'},
            'checkers': {'type': 'grid', 'complexity': 3},
            'floral': {'type': 'organic', 'complexity': 5},
            'geometric': {'type': 'shapes', 'complexity': 4}
        }
        
    def _load_color_palettes(self) -> Dict:
        """Load predefined color palettes"""
        return {
            'monochrome': [(0, 0, 0), (255, 255, 255)],
            'earth_tones': [(139, 90, 43), (205, 133, 63), (222, 184, 135)],
            'ocean': [(0, 105, 148), (0, 150, 199), (72, 202, 228)],
            'sunset': [(255, 94, 77), (255, 175, 123), (253, 255, 182)],
            'forest': [(34, 139, 34), (107, 142, 35), (154, 205, 50)]
        }
        
    def create_new_design(self, base_template: str = 'tshirt') -> Dict:
        """
        Create a new design from a base template.
        
        Args:
            base_template: Type of garment template (tshirt, pants, dress, etc.)
            
        Returns:
            New design dictionary
        """
        design = {
            'id': len(self.design_history),
            'template': base_template,
            'colors': {'primary': (255, 255, 255), 'secondary': (0, 0, 0)},
            'pattern': 'solid',
            'style': 'casual',
            'modifications': [],
            'dimensions': self._get_template_dimensions(base_template)
        }
        
        self.current_design = design
        self.design_history.append(design.copy())
        
        return design
        
    def _get_template_dimensions(self, template: str) -> Dict:
        """Get default dimensions for a template"""
        templates = {
            'tshirt': {'chest': 100, 'length': 70, 'sleeve': 20},
            'pants': {'waist': 80, 'length': 100, 'leg_width': 25},
            'dress': {'bust': 90, 'waist': 75, 'length': 90},
            'jacket': {'chest': 105, 'length': 75, 'sleeve': 65}
        }
        return templates.get(template, {'default': 100})
        
    def change_color(self, color_type: str, color: Tuple[int, int, int]):
        """
        Change the color of the design.
        
        Args:
            color_type: Type of color (primary, secondary, accent)
            color: RGB color tuple
        """
        if not self.current_design:
            raise ValueError("No active design. Create a new design first.")
            
        if color_type not in self.current_design['colors']:
            self.current_design['colors'][color_type] = color
        else:
            old_color = self.current_design['colors'][color_type]
            self.current_design['colors'][color_type] = color
            
        self.current_design['modifications'].append({
            'type': 'color_change',
            'color_type': color_type,
            'new_color': color
        })
        
    def apply_pattern(self, pattern_name: str, settings: Optional[Dict] = None):
        """
        Apply a pattern to the design.
        
        Args:
            pattern_name: Name of the pattern
            settings: Optional pattern-specific settings
        """
        if not self.current_design:
            raise ValueError("No active design. Create a new design first.")
            
        if pattern_name not in self.available_patterns:
            raise ValueError(f"Unknown pattern: {pattern_name}")
            
        self.current_design['pattern'] = pattern_name
        self.current_design['pattern_settings'] = settings or {}
        
        self.current_design['modifications'].append({
            'type': 'pattern_application',
            'pattern': pattern_name,
            'settings': settings
        })
        
    def adjust_dimensions(self, dimension: str, value: float):
        """
        Adjust specific dimensions of the design.
        
        Args:
            dimension: Name of dimension to adjust
            value: New value for the dimension
        """
        if not self.current_design:
            raise ValueError("No active design. Create a new design first.")
            
        if 'dimensions' not in self.current_design:
            self.current_design['dimensions'] = {}
            
        old_value = self.current_design['dimensions'].get(dimension, 0)
        self.current_design['dimensions'][dimension] = value
        
        self.current_design['modifications'].append({
            'type': 'dimension_adjustment',
            'dimension': dimension,
            'old_value': old_value,
            'new_value': value
        })
        
    def add_embellishment(self, embellishment_type: str, position: Tuple[float, float], 
                         size: float = 1.0):
        """
        Add an embellishment to the design.
        
        Args:
            embellishment_type: Type of embellishment (button, zipper, pocket, etc.)
            position: Position as (x, y) coordinates
            size: Size multiplier
        """
        if not self.current_design:
            raise ValueError("No active design. Create a new design first.")
            
        if 'embellishments' not in self.current_design:
            self.current_design['embellishments'] = []
            
        embellishment = {
            'type': embellishment_type,
            'position': position,
            'size': size,
            'id': len(self.current_design['embellishments'])
        }
        
        self.current_design['embellishments'].append(embellishment)
        
        self.current_design['modifications'].append({
            'type': 'embellishment_added',
            'embellishment': embellishment
        })
        
    def apply_color_palette(self, palette_name: str):
        """
        Apply a predefined color palette to the design.
        
        Args:
            palette_name: Name of the color palette
        """
        if not self.current_design:
            raise ValueError("No active design. Create a new design first.")
            
        if palette_name not in self.color_palettes:
            raise ValueError(f"Unknown palette: {palette_name}")
            
        palette = self.color_palettes[palette_name]
        
        if len(palette) > 0:
            self.current_design['colors']['primary'] = palette[0]
        if len(palette) > 1:
            self.current_design['colors']['secondary'] = palette[1]
        if len(palette) > 2:
            self.current_design['colors']['accent'] = palette[2]
            
        self.current_design['modifications'].append({
            'type': 'palette_application',
            'palette': palette_name
        })
        
    def undo_last_modification(self) -> bool:
        """
        Undo the last modification to the design.
        
        Returns:
            True if undo was successful
        """
        if not self.current_design:
            return False
            
        modifications = self.current_design.get('modifications', [])
        if not modifications:
            return False
            
        # Remove last modification from the list
        modifications.pop()
        
        # Rebuild design state by reapplying all modifications except the last one
        # This is a simplified implementation - in a real system, you'd reconstruct
        # the design by replaying the modification history
        
        return True
        
    def get_design_summary(self) -> Dict:
        """
        Get a summary of the current design.
        
        Returns:
            Dictionary with design summary
        """
        if not self.current_design:
            return {'status': 'No active design'}
            
        return {
            'template': self.current_design.get('template', 'unknown'),
            'pattern': self.current_design.get('pattern', 'none'),
            'colors': self.current_design.get('colors', {}),
            'modifications_count': len(self.current_design.get('modifications', [])),
            'embellishments_count': len(self.current_design.get('embellishments', []))
        }
        
    def export_design(self) -> Dict:
        """
        Export the current design for use in other systems.
        
        Returns:
            Complete design data
        """
        if not self.current_design:
            raise ValueError("No active design to export")
            
        return self.current_design.copy()
        
    def generate_variations(self, count: int = 3) -> List[Dict]:
        """
        Generate design variations based on current design.
        
        Args:
            count: Number of variations to generate
            
        Returns:
            List of design variations
        """
        if not self.current_design:
            raise ValueError("No active design. Create a new design first.")
            
        variations = []
        
        for i in range(count):
            variation = self.current_design.copy()
            variation['id'] = f"{self.current_design['id']}_var_{i}"
            
            # Modify colors slightly
            if 'colors' in variation:
                for color_type, color in variation['colors'].items():
                    # Add random variation to color
                    new_color = tuple(
                        max(0, min(255, c + np.random.randint(-30, 30))) 
                        for c in color
                    )
                    variation['colors'][color_type] = new_color
                    
            variations.append(variation)
            
        return variations
