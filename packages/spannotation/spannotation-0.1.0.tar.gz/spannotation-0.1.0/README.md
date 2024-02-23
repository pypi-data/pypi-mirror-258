## Description of software
The package introduces a novel approach to image annotation and segmentation, requiring users to select just three key points on an image. These points define a triangular area representing the region of interest, which the algorithm then uses to generate a binary mask. This mask distinctly categorizes the image into two classes: drivable and non-drivable regions.

## Key applications of this package include:

1. Row Crop Management: In agricultural settings, such as cornfields, the package can segment row crops, identifying drivable paths for farm machinery and ensuring efficient navigation through the fields.
2. Off-Road Navigation: For off-road scenarios, like dirt tracks, the tool can demarcate navigable paths, assisting in the planning and navigation of off-road vehicles.
3. On-Road Navigation: In typical urban or rural roads, the package can be used to distinguish the actual road (drivable region) from its surroundings (non-drivable regions, including shoulders and adjacent land), aiding in basic navigation tasks.

This tool is particularly useful for researchers and practitioners in autonomous vehicle navigation, agricultural robotics, and geographic information systems (GIS), where accurate and efficient image segmentation is critical.

## Installation
To install SPAnnotation, simply use pip: 

pip install spannotation

## Usage
Here's a quick example of how to use SPAnnotation:
```python
from spannotation import SpAnnotator
# Example code demonstrating how to use the package
""" i will include this after pip has been set up"""

## Examples
### Example 1: Row Crop Segmentation
# Description and code example

### Example 2: Off-Road Navigation
# Description and code example


## Contributing
Contributions to SPAnnotation are welcome! Please read our [contributing guidelines](LINK_TO_CONTRIBUTING_GUIDELINES) for details.



## License
SPAnnotation is released under the [MIT License](https://opensource.org/license/mit).


##Contact Info
Please reach out via [LinkedIn, email, phone]






