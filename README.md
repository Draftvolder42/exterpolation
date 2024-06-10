# [Simple vector exterpolation program]
**Simple vector exterpolation program with moving target.**
**Use three points for exterpolation.**
### Files:
<ul>
   <li> <p> <h3> interface.py </p> </h3> button working interface </li>
   <li> <p> <h3> main.py </p> </h3> main program </li>
   <li> <p> <h3> radar.py </p> </h3> class for radar </li>
   <li> <p> <h3> vec.py </p> </h3> class for vector </li>
</ul>

### How to test:
<p>
-In the center of the screen you have a radar with scanning area. When radar ray hit the target, a new position is calculated.
</p>
<p>
-The white circles is the points of the taget.
</p>
<p>
-You can rotate the target with 'a' and 'd' keys.
</p>
<p>
-The red line is exterpolated "prediction" vector (prediction vector activates when target have differece between old and new calculated angles).
</p>
<p>
-The green line is actually exterpolated vector.
</p>

### Parameters:
**All parameters in `config.py`**
<p>
-FPS - frames per second
</p>
<p>
-WIDTH - screen width
</p>
<p>
-HEIGHT - screen height
</p>

