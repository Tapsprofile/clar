"""AI-based look and feel assessment system"""

import numpy as np
from typing import Dict, List, Optional


class LookFeelAssessor:
    """
    AI-based system to assess the look and feel of clothing designs.
    
    Evaluates aesthetic qualities, style matching, and material feel predictions.
    """
    
    def __init__(self):
        """Initialize the Look and Feel Assessor"""
        self.style_database = self._load_style_database()
        self.material_properties = {}
        
    def _load_style_database(self) -> Dict:
        """Load database of style references"""
        return {
            'casual': {'keywords': ['relaxed', 'comfortable', 'everyday'], 'score': 0},
            'formal': {'keywords': ['elegant', 'professional', 'refined'], 'score': 0},
            'sporty': {'keywords': ['athletic', 'dynamic', 'active'], 'score': 0},
            'trendy': {'keywords': ['fashionable', 'modern', 'stylish'], 'score': 0}
        }
        
    def assess_visual_appeal(self, garment_image: np.ndarray) -> Dict:
        """
        Assess the visual appeal of a garment design.
        
        Args:
            garment_image: Image of the garment
            
        Returns:
            Dictionary with visual appeal scores
        """
        # Analyze color distribution
        color_score = self._analyze_colors(garment_image)
        
        # Analyze proportions
        proportion_score = self._analyze_proportions(garment_image)
        
        # Analyze symmetry
        symmetry_score = self._analyze_symmetry(garment_image)
        
        overall_score = (color_score + proportion_score + symmetry_score) / 3
        
        return {
            'overall_appeal': overall_score,
            'color_harmony': color_score,
            'proportions': proportion_score,
            'symmetry': symmetry_score,
            'rating': self._get_rating(overall_score)
        }
        
    def _analyze_colors(self, image: np.ndarray) -> float:
        """Analyze color harmony in the image"""
        if len(image.shape) != 3 or image.shape[2] != 3:
            return 50.0
            
        # Calculate color diversity and harmony
        # Simplified implementation
        mean_color = np.mean(image, axis=(0, 1))
        std_color = np.std(image, axis=(0, 1))
        
        # Score based on color variation (not too bland, not too chaotic)
        score = 100 - min(np.mean(std_color), 50)
        return float(score)
        
    def _analyze_proportions(self, image: np.ndarray) -> float:
        """Analyze design proportions"""
        # Simplified proportion analysis
        height, width = image.shape[:2]
        aspect_ratio = height / width if width > 0 else 1.0
        
        # Ideal aspect ratio for clothing is around 1.5-2.0
        ideal_ratio = 1.75
        ratio_diff = abs(aspect_ratio - ideal_ratio)
        
        score = max(0, 100 - ratio_diff * 50)
        return float(score)
        
    def _analyze_symmetry(self, image: np.ndarray) -> float:
        """Analyze symmetry in the design"""
        # Simplified symmetry check
        height, width = image.shape[:2]
        mid = width // 2
        
        if mid == 0:
            return 50.0
            
        left_half = image[:, :mid]
        right_half = image[:, mid:mid+left_half.shape[1]]
        
        # Flip right half for comparison
        right_flipped = np.fliplr(right_half)
        
        # Calculate similarity
        if left_half.shape == right_flipped.shape:
            difference = np.mean(np.abs(left_half.astype(float) - right_flipped.astype(float)))
            score = max(0, 100 - difference / 2.55)
        else:
            score = 50.0
            
        return float(score)
        
    def _get_rating(self, score: float) -> str:
        """Convert numerical score to rating"""
        if score >= 90:
            return 'Excellent'
        elif score >= 75:
            return 'Good'
        elif score >= 60:
            return 'Fair'
        else:
            return 'Needs Improvement'
            
    def analyze_style_match(self, design_features: Dict, target_style: str) -> Dict:
        """
        Analyze how well a design matches a target style.
        
        Args:
            design_features: Dictionary of design features
            target_style: Target style category
            
        Returns:
            Style matching analysis
        """
        if target_style not in self.style_database:
            raise ValueError(f"Unknown style: {target_style}")
            
        style_data = self.style_database[target_style]
        
        # Calculate match score based on features
        match_score = 0.0
        matched_features = []
        
        for keyword in style_data['keywords']:
            if keyword in str(design_features.values()).lower():
                match_score += 25
                matched_features.append(keyword)
                
        match_score = min(100, match_score)
        
        return {
            'target_style': target_style,
            'match_score': match_score,
            'matched_features': matched_features,
            'confidence': match_score / 100
        }
        
    def predict_material_feel(self, material_type: str) -> Dict:
        """
        Predict how a material will feel based on its type.
        
        Args:
            material_type: Type of material (cotton, silk, polyester, etc.)
            
        Returns:
            Predicted material feel properties
        """
        material_database = {
            'cotton': {
                'softness': 80,
                'breathability': 90,
                'stretch': 40,
                'durability': 70,
                'texture': 'smooth and natural'
            },
            'silk': {
                'softness': 95,
                'breathability': 85,
                'stretch': 30,
                'durability': 50,
                'texture': 'luxurious and smooth'
            },
            'polyester': {
                'softness': 60,
                'breathability': 40,
                'stretch': 70,
                'durability': 90,
                'texture': 'smooth and synthetic'
            },
            'wool': {
                'softness': 70,
                'breathability': 75,
                'stretch': 50,
                'durability': 80,
                'texture': 'warm and textured'
            }
        }
        
        material_lower = material_type.lower()
        if material_lower in material_database:
            return material_database[material_lower]
        else:
            # Default prediction for unknown materials
            return {
                'softness': 50,
                'breathability': 50,
                'stretch': 50,
                'durability': 50,
                'texture': 'unknown'
            }
            
    def generate_aesthetic_report(self, garment_data: Dict) -> str:
        """
        Generate a comprehensive aesthetic report.
        
        Args:
            garment_data: Complete garment data including images and features
            
        Returns:
            Formatted aesthetic report as string
        """
        report_lines = [
            "=== Aesthetic Assessment Report ===",
            ""
        ]
        
        if 'image' in garment_data:
            visual_assessment = self.assess_visual_appeal(garment_data['image'])
            report_lines.extend([
                f"Overall Appeal: {visual_assessment['rating']} ({visual_assessment['overall_appeal']:.1f}/100)",
                f"Color Harmony: {visual_assessment['color_harmony']:.1f}/100",
                f"Proportions: {visual_assessment['proportions']:.1f}/100",
                f"Symmetry: {visual_assessment['symmetry']:.1f}/100",
                ""
            ])
            
        if 'material' in garment_data:
            material_feel = self.predict_material_feel(garment_data['material'])
            report_lines.extend([
                "Material Feel Prediction:",
                f"  Softness: {material_feel['softness']}/100",
                f"  Breathability: {material_feel['breathability']}/100",
                f"  Stretch: {material_feel['stretch']}/100",
                f"  Durability: {material_feel['durability']}/100",
                f"  Texture: {material_feel['texture']}",
                ""
            ])
            
        return "\n".join(report_lines)
