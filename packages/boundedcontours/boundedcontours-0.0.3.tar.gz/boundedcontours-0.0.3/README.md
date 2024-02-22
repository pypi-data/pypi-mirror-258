Gaussian smoothing for 2D arrays where some condition must be maintained e.g. x>y. In the default setting this is achieved by reflection about the boundary before the kernel convolution. See the examples directory.

To install and be able to run the examples:
```bash
python -m pip install 'boundedcontours[examples]'
```

Or from source:
```bash
git clone https://github.com/millsjc/boundedcontours
cd boundedcontours
python -m pip install '.[examples]'
```