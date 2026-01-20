#!/usr/bin/env python3
"""
Quick start example for CLAR - focusing on fit analysis.
"""

from clar import FitAnalyzer


def main():
    print("=== CLAR Fit Analysis Quick Start ===\n")
    
    # Create fit analyzer
    analyzer = FitAnalyzer()
    
    # Set your body measurements (in centimeters)
    body = {
        'chest': 92,
        'waist': 78,
        'hips': 95,
        'shoulder_width': 44,
        'arm_length': 58
    }
    analyzer.set_body_measurements(body)
    
    # Set garment measurements
    garment = {
        'chest': 98,
        'waist': 84,
        'hips': 100
    }
    analyzer.set_garment_measurements(garment)
    
    # Analyze fit
    results = analyzer.analyze_fit()
    
    # Display results
    print(f"Overall Fit Score: {results['overall_fit_score']:.1f}/100\n")
    
    print("Fit by Area:")
    for area, data in results['areas'].items():
        print(f"  {area.capitalize()}: {data['score']:.1f}/100 ({data['status']})")
        print(f"    Difference: {data['difference_cm']:.1f}cm")
    
    print("\nRecommendations:")
    for rec in results['recommendations']:
        print(f"  • {rec}")
    
    # Suggest size
    suggested_size = analyzer.suggest_size()
    print(f"\nSuggested Size: {suggested_size}")


if __name__ == "__main__":
    main()
