English | [日本語](BUILD_ja.md)

# Building GOTOKU-55

![top](topview.jpg)

## Parts needed

### Electronics
- [Ploopy Adept PCB](https://github.com/ploopyco/adept-trackball/tree/master/hardware/electronics)
- [Firmware](https://github.com/ploopyco/qmk_firmware)
- PMW3360 optical sensor
  - LM19-LSI lens
- USB-C cable

Buying the Adept kit gets you all of the electronics.


### Mechanical parts
- 55 mm ball
- M2x10mm countersunk screws x4
- Ball supports (choose one)
  - SMR63ZZ ball bearings x3 (ball bearing version)
  - BTUs x3 (BTU version, see below)
- (Optional) Self-adhesive rubber feet, 8 mm diameter, 1.6 mm high, x4

If you hesitate to buy an expensive 55 mm ball right away, a 55 mm table tennis practice ball is a cheap alternative. It is very light, and it feels unusual because you feel no inertia at all. It might even turn out to be the best choice.

Ball bearings rust quickly unless they are stainless steel. I recommend NSK ones.

#### BTU
Like ploopy-adept-small-btu, the BTU version uses Bosch Rexroth KU-B8 in place of the ball bearings.  
However, I have so far tested it only with the IGUCHI IS-05SNM. I have not tested it with the KU-B8.  
The adept-anyball/mod repository has [adapters](https://github.com/adept-anyball/mod/tree/master/adapters) that let you use other BTUs, static supports such as ceramic balls, and more. Some adapters are not recommended for large, heavy balls, so check the notes for each adapter.  
Which parts you can get varies a lot by country and region, so first find out what is available to you. The KU-B8 is not the only option.

### 3D printed parts
- [Bearing dowel (axle)](https://github.com/ploopyco/classic-2-trackball/tree/master/hardware/mechanicals) (ball bearing version only)
- [Bearing press jig](https://github.com/ploopyco/classic-2-trackball/tree/master/hardware/mechanicals) (ball bearing version only)
- [GOTOKU arm](../3d-model/) (choose one)
  - Ball bearing, one-piece version, printed in PLA
    - `gotoku55-arm`
  - Ball bearing, split version, metal arm and PLA floor
    - `gotoku55-arm-split-metal` (metal)
    - `gotoku55-arm-split-floor` (PLA)
  - BTU, split version, metal arm and PLA floor
    - `gotoku55-btu-arm` (metal)
    - `gotoku55-arm-split-floor` (PLA)
- Case top and bottom (choose one set)
  - [small-btu v4 case top and bottom](https://github.com/adept-anyball/ploopy-adept-small-btu/tree/main/v4)
  - [GOTOKU case top and bottom](../3d-model/)
    - `gotoku55-case-top`, `gotoku55-case-bottom`

The parts must be printed in the right orientation. As a rule, the large flat face goes on the build plate.

The arm parts also come as STEP files for metal printing. The GOTOKU case bottom also comes as a STEP file. The GOTOKU case top is STL only.

`gotoku55-assembled` and `gotoku55-btu-assembled` show the GOTOKU case, an arm and a 55 mm ball, put together. They are for checking the look. They are not for printing.

### Metal parts
I recommend the split version of the arm, printed in metal with SLM. A PLA arm bends outward under the weight of the 55 mm ball and your palm. A metal arm does not bend. I had mine printed in stainless steel 316L.

Apart from the bending, a metal arm is not required. The bending is not pleasant, but it does not make the trackball unusable.

If you use BTUs, keep in mind that, depending on the print accuracy, a BTU such as the KU-B8 may not fit. The BTU pockets have the same dimensions as the official v4: a 12.7 mm bore for the 12.6 mm body of the KU-B8, and a 17.2 mm counterbore for its 17 mm flange. That leaves only 0.1 to 0.2 mm of clearance in diameter, and unlike plastic, metal will not stretch a little when you press the BTU in.  
If you use an adapter with a BTU smaller than the KU-B8, the plastic adapter sits in between, which eases this problem.

## Assembly

### Assembling the bearings
Use the jig to press a dowel into each bearing. It probably makes no difference in practice if the dowel is not perfectly centered.

Press the bearings into the GOTOKU arm part. The jig is handy for this. Once they are in, check that they spin smoothly.

Each post of the arm has a 3 mm hole on its outer side. If something goes wrong, push a toothpick into this hole to push the bearing out from behind, and start over.

### Assembling the case
If you use the split version of the arm, first put the PLA floor into the metal arm from below. The small tab on the edge of the floor goes toward the front post. The floor is held in place by the sensor lens, so it falls out when you lift the arm out of the case.

Fit the GOTOKU arm into the case top.

![trim](need_trim.jpg)

If the fit is tight, check whether the bottom face of the print has flared out into a thin lip. You may need to trim it a little with a file or a knife.

If the ball does not track or the buttons do not press properly, the case may need adjusting.
3D printed parts are not strong enough to be screwed together many times, so test that everything works before you drive the screws in.

### Sharing your build
An expensive trackball ball may reflect your room, or your face.
Check before you post photos of your trackball on social media.
