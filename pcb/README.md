English | [日本語](README_ja.md)

# GOTOKU PCB v1

This is a modified version of the Ploopy Madromys PCB (R1.001), the main board of the Ploopy Adept trackball.
The goal is to order the board with assembly (PCBA) from JLCPCB, so that no hand soldering is needed for the small parts.

**This is NOT an official Ploopy product. Do not ask Ploopy for support.**

This board is not built and not tested yet.

## Variants

There are two variants. They differ only in the USB-C connector.

| Folder | USB-C connector | Notes |
|---|---|---|
| [original](original/) | JAE DX07S016JA1R1500 (LCSC C3197885) | Same connector and routing as the original board. |
| [hro](hro/) | HRO TYPE-C-31-M-12 (LCSC C165948) | Slightly cheaper at JLCPCB. Routing around the connector was changed by hand. |

Each folder has these files:

- `*.kicad_pcb` is the board data for KiCad.
- `*-gerber.zip` is the Gerber and drill data.
- `*-BOM-JLC.csv` and `*-CPL-JLC.csv` are the BOM and the placement file for JLCPCB assembly.
- `*-gerber-preview.png` is a preview image of the Gerber data.

## Ordering at JLCPCB

- 4 layers, 0.8 mm thickness
- Assemble top side
- Upload the BOM and the CPL file of the same variant.

Parts without an LCSC number in the BOM are not assembled by JLCPCB.
These are the switches (D2LS-21) and the optical sensor (PMW3360DM-T2QU). Solder them by hand.

## Changes from the original

The original data is the Altium project in [ploopyco/adept-trackball](https://github.com/ploopyco/adept-trackball) (`hardware/electronics/PCBs/Madromys`, commit `2ec4576`).
Only the PCB was converted. The schematic was not converted. See the original schematic PDF for the circuit.

### Conversion from Altium to KiCad

The board was converted with the Altium importer of KiCad 7.
These fixes were needed after the conversion.

- The square opening for the optical sensor is now a cutout in the board outline.
- The two locating holes of the USB-C connector are now non-plated holes.
- 10 very short broken arcs in the copper were replaced with straight segments.
- The board thickness is set to 0.8 mm. This value comes from the Altium layer stack.

### Parts that are not mounted

These parts are marked as "DNP" (do not populate). They are removed from the BOM and the CPL file. Their pads stay on the board.

| Designator | Part | Reason |
|---|---|---|
| LED.D.1, LED.D.3 | Addressable RGB LED | The Ploopy firmware does not use them. In most cases the LEDs cannot be seen from outside. |
| LED.C.20, LED.C.23, LED.R.9, LED.R.16 | Capacitors and resistors for the LEDs | Not needed without the LEDs. |
| USB.R.12, USB.R.14 | 10k resistor on CC1 and CC2 | The original uses two 10k resistors in parallel on each CC line. This board uses one 5.1k resistor instead. |
| MCU.J.1 | 2-pin header | No header is mounted, same as the original product. The two holes are used to start the bootloader. See below. |

### Changed values and substitute parts

| Designator | Original | This board |
|---|---|---|
| USB.R.13, USB.R.15 | 10k 1% | 5.1k 1% (one resistor for each CC line) |
| USB.Z.1 | IP4220CZ6 (ESD protection) | SRV05-4 (LCSC C384887). Same pinout. |
| REG.U.4 | AP2204K-1.8 | AP2112K-1.8 (LCSC C176944). Same pinout. |
| MCU.Y.1 | RH100-12.000-16-3030 (12 MHz, 16 pF) | X322512MSB4SI (12 MHz, 20 pF, LCSC C9002). The load capacitors stay at 18 pF. |

REG.C.15 (100 pF) is marked as "not fitted" in the BoM variant of the original project.
On this board it is mounted.

Other passive parts were replaced with common LCSC parts of the same value and size.

### Silkscreen

- The board name "Madromys R1.001 / August 2023" was changed to "GOTOKU PCB v1".
- The label "MCH.FID.1" was hidden.
- A logo and a notice of the modification were added on the top side.

### HRO variant only

The HRO connector has a different pad layout. These changes were made only in the `hro` variant.

- The connector footprint was replaced with `USB_C_Receptacle_HRO_TYPE-C-31-M-12` from the KiCad library. The position and the direction are the same as the original connector.
- The D+, D-, CC1, CC2 and VBUS traces near the connector were changed to fit the new pads.
- One VBUS via was moved, and one GND via under the connector was removed.
- The copper pour was cleared around the new traces and pads.

The connections and the clearances near the connector were checked with a script.
**A full DRC has not been run yet. Run the DRC in KiCad 8 or later before you order this variant.**
`Madromys-usb-area-orig-vs-hro.png` shows the area around the connector in both variants.

## Starting the bootloader

You do not need this for the first firmware upload.
A new board has an empty flash memory, so the RP2040 starts in the bootloader (BOOTSEL mode) automatically.

To update the firmware later, hold the bottom left button (matrix [0,0]) while you plug in the USB cable.

If the firmware is broken and the button does not work, use the two holes of MCU.J.1 near LED.D.3.
Connect the two holes with metal tweezers, and plug in the USB cable at the same time.
One hole is GND. The other hole is connected to the chip select line of the flash memory through a 1k resistor.

## License

The files in this folder are licensed under the CERN Open Hardware Licence Version 2, Strongly Reciprocal (CERN-OHL-S-2.0).
See [LICENSE](LICENSE).
This is different from the rest of this repository, which uses GPL-3.0.

- Original design: Ploopy Madromys R1.001 (Ploopy Adept) by Ploopy Corporation, licensed under CERN-OHL-S-2.0.
  Source: https://github.com/ploopyco/adept-trackball
- Modifications: Copyright (C) 2026 Kotaro WAJIKI. Modified on 2026-10-11. The changes are listed in "Changes from the original" above.
- Source Location of this modified design: https://github.com/beatenavenue/hw_gotoku55-trackball/tree/main/pcb

This design is provided "as is", without any warranty. See section 6 of the license.
