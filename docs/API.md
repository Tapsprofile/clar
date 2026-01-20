# API Reference

## VRInterface

### Class: `VRInterface(resolution=(1920, 1080))`

VR Interface for visualizing and interacting with 3D garments.

#### Methods

##### `initialize_vr_environment() -> bool`
Initialize the VR environment for garment visualization.

**Returns:** `True` if successful

##### `load_garment_model(garment_data: Dict) -> bool`
Load a 3D garment model into VR.

**Parameters:**
- `garment_data`: Dictionary with mesh, texture, and metadata

**Returns:** `True` if successful

##### `render_scene() -> np.ndarray`
Render the current VR scene.

**Returns:** Rendered scene as numpy array

##### `apply_physics(gravity=9.8, wind=None)`
Apply physics simulation to garments.

**Parameters:**
- `gravity`: Gravity strength (default: 9.8)
- `wind`: Wind vector as (x, y, z) tuple

##### `set_camera_position(position, rotation=(0, 0, 0))`
Set VR camera position and rotation.

**Parameters:**
- `position`: Camera position as (x, y, z)
- `rotation`: Camera rotation in degrees

---

## FitAnalyzer

### Class: `FitAnalyzer(model_path=None)`

AI-based system for analyzing clothing fit.

#### Methods

##### `set_body_measurements(measurements: Dict[str, float])`
Set body measurements for fit analysis.

**Required keys:** chest, waist, hips, shoulder_width, arm_length

##### `set_garment_measurements(measurements: Dict[str, float])`
Set garment measurements for comparison.

##### `analyze_fit() -> Dict`
Analyze garment fit on the body.

**Returns:** Dictionary with fit scores and recommendations

##### `suggest_size() -> str`
Suggest the best size based on measurements.

**Returns:** Size string (XS, S, M, L, XL)

---

## DesignCustomizer

### Class: `DesignCustomizer()`

Tools for customizing clothing designs.

#### Methods

##### `create_new_design(base_template='tshirt') -> Dict`
Create a new design from a template.

**Parameters:**
- `base_template`: Template type (tshirt, pants, dress, jacket)

**Returns:** New design dictionary

##### `change_color(color_type: str, color: Tuple[int, int, int])`
Change design color.

**Parameters:**
- `color_type`: Type (primary, secondary, accent)
- `color`: RGB tuple

##### `apply_pattern(pattern_name: str, settings=None)`
Apply a pattern to the design.

**Available patterns:** solid, stripes, checkers, floral, geometric

##### `apply_color_palette(palette_name: str)`
Apply a predefined color palette.

**Available palettes:** monochrome, earth_tones, ocean, sunset, forest

##### `add_embellishment(embellishment_type: str, position: Tuple[float, float], size=1.0)`
Add an embellishment to the design.

##### `export_design() -> Dict`
Export the current design.

---

## LookFeelAssessor

### Class: `LookFeelAssessor()`

AI-based system for assessing look and feel.

#### Methods

##### `assess_visual_appeal(garment_image: np.ndarray) -> Dict`
Assess visual appeal of a garment.

**Returns:** Dictionary with appeal scores and ratings

##### `analyze_style_match(design_features: Dict, target_style: str) -> Dict`
Analyze style matching.

**Styles:** casual, formal, sporty, trendy

##### `predict_material_feel(material_type: str) -> Dict`
Predict material feel properties.

**Returns:** Dictionary with softness, breathability, stretch, durability

##### `generate_aesthetic_report(garment_data: Dict) -> str`
Generate comprehensive aesthetic report.

**Returns:** Formatted report string
