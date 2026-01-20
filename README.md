# CLAR - VR AI Clothing Design Tools

**CLAR** is a comprehensive VR AI-based toolkit to support clothing design, fit analysis, and look and feel assessment.

## Features

### 🥽 VR Interface
- 3D garment visualization in virtual reality
- Interactive scene management
- Realistic physics simulation for garment draping
- Camera control and positioning

### 🤖 AI-Powered Fit Analysis
- Intelligent fit scoring based on body measurements
- Pressure point detection
- Size recommendation system
- Detailed fit reports by body area

### 🎨 Design Customization
- Interactive color palette application
- Pattern and texture management
- Embellishment placement
- Design variation generation
- Dimension adjustment tools

### 👗 Look & Feel Assessment
- Visual appeal analysis
- Style matching algorithms
- Material feel prediction
- Aesthetic reporting

## Installation

```bash
pip install -e .
```

Or install dependencies manually:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Fit Analysis

```python
from clar import FitAnalyzer

# Create analyzer
analyzer = FitAnalyzer()

# Set measurements (in cm)
analyzer.set_body_measurements({
    'chest': 92,
    'waist': 78,
    'hips': 95,
    'shoulder_width': 44,
    'arm_length': 58
})

analyzer.set_garment_measurements({
    'chest': 98,
    'waist': 84,
    'hips': 100
})

# Analyze fit
results = analyzer.analyze_fit()
print(f"Fit Score: {results['overall_fit_score']:.1f}/100")
```

### VR Garment Visualization

```python
from clar import VRInterface

# Initialize VR
vr = VRInterface(resolution=(1920, 1080))
vr.initialize_vr_environment()

# Load garment
garment_data = {
    'mesh': garment_mesh,
    'texture': texture_image,
    'material': 'cotton'
}
vr.load_garment_model(garment_data)

# Apply physics
vr.apply_physics(gravity=9.8, wind=(0.5, 0, 0))
```

### Design Customization

```python
from clar import DesignCustomizer

# Create customizer
customizer = DesignCustomizer()

# Create new design
design = customizer.create_new_design('tshirt')

# Customize
customizer.apply_color_palette('ocean')
customizer.apply_pattern('stripes')
customizer.add_embellishment('pocket', (0.2, 0.5))

# Export
final_design = customizer.export_design()
```

### Look and Feel Assessment

```python
from clar import LookFeelAssessor

# Create assessor
assessor = LookFeelAssessor()

# Assess visual appeal
assessment = assessor.assess_visual_appeal(garment_image)
print(f"Rating: {assessment['rating']}")

# Predict material feel
feel = assessor.predict_material_feel('cotton')
print(f"Softness: {feel['softness']}/100")
```

## Examples

Run the comprehensive demo:

```bash
python examples/demo.py
```

Run the quick start example:

```bash
python examples/quick_start.py
```

## Architecture

```
clar/
├── vr/              # VR interface and visualization
│   └── interface.py
├── ai/              # AI-powered analysis tools
│   ├── fit_analyzer.py
│   └── look_feel_assessor.py
├── design/          # Design customization tools
│   └── customizer.py
└── utils/           # Utility functions
    └── __init__.py
```

## Use Cases

- **Fashion Design**: Create and visualize clothing designs in VR
- **E-commerce**: Provide accurate fit recommendations online
- **Virtual Try-On**: Allow customers to see how clothes fit before purchase
- **Manufacturing**: Optimize garment patterns for better fit
- **Personal Styling**: Match clothing styles to individual preferences

## Requirements

- Python 3.8+
- NumPy
- OpenCV
- Pillow
- scikit-learn
- TensorFlow

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
