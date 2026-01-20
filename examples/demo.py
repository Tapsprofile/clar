#!/usr/bin/env python3
"""
Example script demonstrating the CLAR VR AI-based clothing design tools.

This script shows how to:
1. Initialize VR interface
2. Load and analyze garment fit
3. Customize design
4. Assess look and feel
"""

import numpy as np
from clar import VRInterface, FitAnalyzer, DesignCustomizer, LookFeelAssessor


def main():
    print("=== CLAR VR AI Clothing Design Demo ===\n")
    
    # 1. Initialize VR Interface
    print("1. Initializing VR Environment...")
    vr = VRInterface(resolution=(1920, 1080))
    vr.initialize_vr_environment()
    print("   ✓ VR environment initialized\n")
    
    # 2. Load a garment model
    print("2. Loading Garment Model...")
    garment_data = {
        'mesh': np.random.rand(100, 3),  # Simplified mesh data
        'texture': None,
        'material': 'cotton',
        'position': [0, 0, 0]
    }
    vr.load_garment_model(garment_data)
    print("   ✓ Garment loaded into VR\n")
    
    # 3. Set camera and apply physics
    print("3. Configuring VR Scene...")
    vr.set_camera_position((0, 1.6, -3), (0, 0, 0))
    vr.apply_physics(gravity=9.8, wind=(0.5, 0, 0))
    print("   ✓ Camera positioned and physics applied\n")
    
    # 4. Analyze fit
    print("4. Analyzing Garment Fit...")
    fit_analyzer = FitAnalyzer()
    
    # Set body measurements (in cm)
    body_measurements = {
        'chest': 95,
        'waist': 80,
        'hips': 98,
        'shoulder_width': 45,
        'arm_length': 60
    }
    fit_analyzer.set_body_measurements(body_measurements)
    
    # Set garment measurements
    garment_measurements = {
        'chest': 100,
        'waist': 85,
        'hips': 102
    }
    fit_analyzer.set_garment_measurements(garment_measurements)
    
    # Perform fit analysis
    fit_results = fit_analyzer.analyze_fit()
    print(f"   Overall Fit Score: {fit_results['overall_fit_score']:.1f}/100")
    print(f"   Recommendations:")
    for rec in fit_results['recommendations']:
        print(f"     - {rec}")
    print()
    
    # 5. Customize design
    print("5. Customizing Design...")
    customizer = DesignCustomizer()
    
    # Create a new t-shirt design
    design = customizer.create_new_design('tshirt')
    print(f"   Created design: {design['template']}")
    
    # Apply color palette
    customizer.apply_color_palette('ocean')
    print("   ✓ Applied ocean color palette")
    
    # Add pattern
    customizer.apply_pattern('stripes', {'width': 5, 'orientation': 'horizontal'})
    print("   ✓ Applied stripe pattern")
    
    # Add embellishment
    customizer.add_embellishment('pocket', (0.2, 0.5), size=1.2)
    print("   ✓ Added pocket embellishment")
    
    # Get design summary
    summary = customizer.get_design_summary()
    print(f"   Design Summary: {summary['modifications_count']} modifications made\n")
    
    # 6. Assess look and feel
    print("6. Assessing Look and Feel...")
    assessor = LookFeelAssessor()
    
    # Create a sample garment image
    sample_image = np.random.randint(0, 256, (600, 400, 3), dtype=np.uint8)
    
    # Assess visual appeal
    visual_assessment = assessor.assess_visual_appeal(sample_image)
    print(f"   Visual Appeal: {visual_assessment['rating']}")
    print(f"   Overall Score: {visual_assessment['overall_appeal']:.1f}/100")
    
    # Analyze style match
    design_features = {'cut': 'relaxed', 'fit': 'comfortable'}
    style_match = assessor.analyze_style_match(design_features, 'casual')
    print(f"   Style Match: {style_match['match_score']:.1f}/100 for {style_match['target_style']} style")
    
    # Predict material feel
    material_feel = assessor.predict_material_feel('cotton')
    print(f"   Material Feel (Cotton):")
    print(f"     Softness: {material_feel['softness']}/100")
    print(f"     Breathability: {material_feel['breathability']}/100")
    print(f"     Texture: {material_feel['texture']}")
    print()
    
    # 7. Generate design variations
    print("7. Generating Design Variations...")
    variations = customizer.generate_variations(count=3)
    print(f"   ✓ Generated {len(variations)} design variations\n")
    
    # 8. Export final design
    print("8. Exporting Design...")
    exported_design = customizer.export_design()
    print(f"   ✓ Design exported with ID: {exported_design['id']}\n")
    
    print("=== Demo Complete ===")
    print("\nThe CLAR system successfully demonstrated:")
    print("  • VR environment initialization and garment visualization")
    print("  • AI-based fit analysis with recommendations")
    print("  • Interactive design customization")
    print("  • Look and feel assessment")
    print("  • Design variation generation")


if __name__ == "__main__":
    main()
