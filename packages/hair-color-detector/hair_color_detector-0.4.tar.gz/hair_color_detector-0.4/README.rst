===============================
hair-color-detector
===============================

[pypi](https://pypi.org/project/hair-color-detector/)

This project allows you to get the hair color of a person from an image.

Features
--------

TOPAS is a Monte Carlo tool for particle simulation, designed for medical physics research. It can output two data types:

- **binned**: a quantity (e.g. dose) is accumulated within a binned geometry component
- **ntuple**: multiple data columns are recorded per particle history

This package is able to read both data types, enabling analysis within Python.

Basic Usage
-----------

```python
from hair_color_detector import HairColorDetector
hcd = HairColorDetector()
hcd.get_color('test.png',  save_result=True, n_clusters=10)