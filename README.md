# VarInt Conversion Tools  
**Forensic Utility Suite for VarInt Encoding & Decoding**  
*(CLI & GUI version)*

**Author:** Marc Brandt, mb4n6
**Status:** Stable  
**Version:** 1.0  
**License:** MIT, Research & Training only  

---

## Overview

The VarInt Conversion Tools provide a minimal, reliable workflow for encoding and decoding integer values in VarInt-style formats commonly observed in forensic data structures, LevelDB stores, BIOME-streams, and other binary serialization systems.

Inspired by the style and layout of the *Protobuf Stream Viewer* README, this repository contains:

- A **CLI tool** (`varint_converter.py`)  
- A **GUI tool** (`varint_converter_gui.py`) with PySide6  

Both tools support converting:

- **Integer → VarInt (hex)**
- **VarInt (hex) → Integer**

The GUI automatically uses the CLI conversion functions if they are valid and available.  
Otherwise it falls back to a safe Protobuf-compatible VarInt implementation.

---

## Features

### CLI Conversion Tool (`varint_converter.py`)
- Convert **decimal integers** to **VarInt hex format**
- Convert **VarInt hex sequences** back to integers
- Accepts flexible input formats: `80 01`, `8001`, `0x80 0x01`, `80-01`, `80,01`
- Prints conversion results cleanly and consistently
- Command-line usage similar to other forensic utilities

### GUI Tool (`varint_converter_gui.py`)
- PySide6 graphical interface
- Two conversion modes:
  - **Int → VarInt**
  - **VarInt → Int**
- Real-time validation & error display
- Supports space-separated hex formatting
- Auto-detection of CLI implementation
- Fallback encoding/decoding logic ensures consistent results even when CLI script has errors
- Clean forensic-oriented interface with monospace output view

### Forensic-Ready Design
- Zero external dependencies beyond Python & PySide6  
- No rewriting, no mutation of input files  
- Deterministic output  
- VarInt decoding safeguards against malformed or oversized input  
- Hex normalization for unpredictable input formats  

---

## Installation

### Requirements
- Python 3.10+
- PySide6 (GUI only)

Install PySide6:

```bash
pip install PySide6
```

---

Usage

CLI Usage

Run:

python3 varint_converter.py --Art int --Wert 300 --out

or (VarInt to Int):

python3 varint_converter.py --Art varint --Wert "80 02" --out

---

GUI Usage

Start the GUI:

python3 varint_converter_gui.py

You will see:
	•	Mode selection
	•	Input field
	•	Convert button
	•	Copy output button
	•	Monospace result window

Example input → output:

Input: 300
Output: AC 02

Input: 80 02
Output: 300


---

VarInt Format Notes
	•	Encoding follows the standard 7-bit continuation scheme found in many serialization formats (incl. Protobuf).
	•	Each byte stores:
	•	7 bits of data
	•	1 bit continuation flag (MSB)
	•	The last byte always has MSB = 0
	•	Decoding stops at first byte with MSB cleared

The fallback implementation ensures compatibility where the original CLI functions fail or cannot be loaded.

---

Disclaimer

This utility is designed for:
	•	Training & teaching (digital forensics, serialization formats)
	•	Controlled laboratory work
	•	Reverse engineering of binary data structures

It is not intended for operational casework and does not replace certified forensic tooling.
