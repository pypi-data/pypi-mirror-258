# Coordinate Systems

The `Qseis06a` (raw Fortran code) uses SI Unit System，the coordinate systems as following

Cylindrical (z,r,t):
- z = downward
- r = from source outward
- t = azmuth angle from north to east

Cartesian (x,y,z):  
- x = north
- y = east
- z = downward


# Green Functions

The output of `Qseis06a` is `ex-2`, `ss-2`, `ds-2`, `cl-2`, `fz-2`, `fh-2`, and the extensions of Green's functions' file names, which will be appended by the program automatically: `*.tz`, `*.tr`, `*.tt`, and `*.tv` are for the vertical, radial, tangential, and volume change (for hydrophones) components, respectively. **NOTE:** I didn't use tv (volume) component to compute the synthetic seisgrams.

- `ex-2` is for explosion source

- `fz-2` and `fh-2` are for single force. And I use the following formula to compute the synthetic seisgrams:

![Alt text](note/image-5.png)

- `ex-2`, `ss-2`, `ds-2`, and `cl-2` are for double couple. And `ss` is a vertical strike-slip fault, `ds` is a vertical dip-slip fault source, and `cl` is a dip-slip fault with a dip of 45°, they are the 3 fundamental faults.

However, when I compare the `cl-2` output, I found Prof. Rongjiang use (-0.5/ -0.5/ 1.0/ -- / -- / -- ) for (m11/ m22/ m33/ m12/ m23/ m31) to calculate the green functions, and the standard moment tensor for dip-slip fault with a dip of 45° should be (-1.0/ -1.0/ 2.0/ -- / -- / -- ). So I multiple a factor 2 when I read those gfs into a `shakecore` object.

After correct the `cl` green functions, I use the following formula to compute systhetic seisgrams:

![Alt text](note/image.png)
![Alt text](note/image-1.png)
![Alt text](note/image-2.png)

However, the above formula is not a linear style, we rewrite as following:

![Alt text](note/image-3.png)
![Alt text](note/image-4.png)


# Unit
The `Qseis06a` (raw Fortran code) uses SI Unit System

- The unit of green function is `m` (displacement)

- For explosion synthetic waveform, the unit of `m0` (scalar seismic moment) is `N.m`

- For single force synthetic waveform, the unit of `fx` is `N`

- For double couple synthetic waveform, the unit of `mw` is moment magnitude.

![Alt text](note/image-6.png)

- For moment tensor synthetic waveform. the unit of `mxx` is `N.m`, note that `10^7 dyn = 1 N.m`

# Reference

More information about the synthesize operation is showing in

- Minson, Sarah E., and Douglas S. Dreger. "Stable inversions for complete moment tensors." Geophysical Journal International 174.2 (2008): 585-592.

- Herrmann, R.B. & Hutchensen, K., 1993. Quantiﬁcation of m Lg for small explosions, in Report PL-TR-93-2070, 90 pp., Phillips Laboratory, Hanscom Air Force Base, MA.
