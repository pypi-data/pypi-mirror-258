[![PyPI](https://img.shields.io/pypi/v/lorenz-phase-space?label=pypi%20version)](https://pypi.org/project/lorenz-phase-space/)
[![CircleCI](https://circleci.com/gh/daniloceano/lorenz_phase_space.svg?style=shield)](https://app.circleci.com/pipelines/github/daniloceano/lorenz_phase_space)


# Lorenz Phase Space Visualization


<img src="https://github.com/daniloceano/lorenz_phase_space/assets/56005607/862e0916-4960-4658-b7eb-91f7ad57fe9f" width="550">


## Overview

The Lorenz Phase Space (LPS) visualization tool is designed to analyze and illustrate the dynamics of the Lorenz Energy Cycle in atmospheric science.

This tool offers a unique perspective for studying the intricate processes governing atmospheric energetics and instability mechanisms.
It visualizes the transformation and exchange of energy within the atmosphere, specifically focusing on the interactions between kinetic and potential energy forms as conceptualized by Edward Lorenz.

Key features of the tool include:

- Mixed Mode Visualization: Offers insights into both baroclinic and barotropic instabilities, which are fundamental in understanding large-scale atmospheric dynamics. 
This mode is particularly useful for comprehensively analyzing scenarios where both instabilities are at play.

- Baroclinic Mode: Focuses on the baroclinic processes, highlighting the role of temperature gradients and their impact on atmospheric energy transformations.
This mode is vital for studying weather systems and jet stream dynamics.

- Barotropic Mode: Concentrates on barotropic processes, where the redistribution of kinetic energy is predominant. 
This mode is essential for understanding the horizontal movement of air and its implications on weather patterns.


By utilizing the LPS tool, researchers and meteorologists can delve into the complexities of atmospheric energy cycles, gaining insights into how different energy forms interact and influence weather systems and climate patterns. 
The tool's ability to switch between different modes (mixed, baroclinic, and barotropic) allows for a multifaceted analysis of atmospheric dynamics, making it an invaluable resource in the field of meteorology and climate science.

## Features

- Visualization of data in Lorenz Phase Space.
- Support for different types of Lorenz Phase Spaces: mixed, baroclinic, and barotropic.
- Dynamic adjustment of visualization parameters based on data scale.
- Customizable plotting options for detailed analysis.

## Installation

To use this tool, ensure you have Python installed along with the required libraries: pandas, matplotlib, numpy, and cmocean. You can install these packages using pip:


```pip install pandas matplotlib numpy cmocean```

## Usage

Import the LorenzPhaseSpace class from LPS.py and initialize it with your data. Here's a basic example:

```
from LPS import LorenzPhaseSpace
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Initialize the Lorenz Phase Space plotter
lps = LorenzPhaseSpace(
    x_axis=data['Ck'],
    y_axis=data['Ca'],
    marker_color=data['Ge'],
    marker_size=data['Ke'],
    LPS_type='mixed'  # Choose from 'mixed', 'baroclinic', 'barotropic'
)

# Plot and save the visualization
fig, ax = lps.plot()
plt.savefig('LPS_visualization.png', dpi=300)
```


## Contributing

Contributions to the LPS project are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or further assistance with the Lorenz Phase Space project, please reach out to danilo.oceano@gmail.com.
