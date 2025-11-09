#!/usr/bin/env python3
"""
VarInt Converter – GUI
"""
import sys
import re
import importlib.util

def _load_cli_module():
    try:
        spec = importlib.util.spec_from_file_location("varint_cli", "varint_converter.py")
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  
            return mod
    except Exception as e:
        return None
    return None

_cli = _load_cli_module()

def _encode_varint_protobuf(n: int) -> bytes:
    if n < 0:
        n &= (1 << 64) - 1  
    out = bytearray()
    while True:
        to_write = n & 0x7F
        n >>= 7
        if n:
            out.append(to_write | 0x80)
        else:
            out.append(to_write)
            break
    return bytes(out)

def _decode_varint_protobuf(b: bytes) -> int:
    shift = 0
    result = 0
    for i, byte in enumerate(b, 1):
        result |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            return result
        shift += 7
        if shift > 70:
            raise ValueError("Varint is too long or malformed")
    raise ValueError("Incomplete varint: no terminating byte without continuation bit")

def _bytes_from_hex_str(s: str) -> bytes:
    s = s.strip()
    if not s:
        return b""
    s = s.lower().replace("0x", "").replace(",", " ").replace("-", " ").replace(";", " ")
    s = re.sub(r"\s+", " ", s).strip()
    if " " in s:
        parts = s.split(" ")
        hex_joined = "".join(parts)
    else:
        hex_joined = s
    if len(hex_joined) % 2 != 0:
        raise ValueError("Hex input must have even number of characters")
    return bytes.fromhex(hex_joined)

def _hex_str(b: bytes, spaced=True) -> str:
    if spaced:
        return " ".join(f"{x:02X}" for x in b)
    return b.hex().upper()

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QButtonGroup, QTextEdit, QCheckBox, QMessageBox
)
from PySide6.QtGui import QFont, QClipboard
from PySide6.QtCore import Qt

class VarintConverterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VarInt Converter – GUI")
        self.setMinimumWidth(700)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("VarInt Converter")
        f = QFont()
        f.setPointSize(16)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        mode_row = QHBoxLayout()
        mode_label = QLabel("Mode:")
        self.rb_int2var = QRadioButton("Int → VarInt (hex)")
        self.rb_var2int = QRadioButton("VarInt (hex) → Int")
        self.rb_int2var.setChecked(True)
        group = QButtonGroup(self)
        group.addButton(self.rb_int2var)
        group.addButton(self.rb_var2int)
        mode_row.addWidget(mode_label)
        mode_row.addWidget(self.rb_int2var)
        mode_row.addWidget(self.rb_var2int)
        mode_row.addStretch(1)
        layout.addLayout(mode_row)

        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("Enter integer (e.g., 300) or varint hex (e.g., 80 02)...")
        layout.addWidget(QLabel("Input:"))
        layout.addWidget(self.input_edit)

        opts_row = QHBoxLayout()
        self.cb_hex_spaces = QCheckBox("Space-separated hex output")
        self.cb_hex_spaces.setChecked(True)
        opts_row.addWidget(self.cb_hex_spaces)
        opts_row.addStretch(1)
        layout.addLayout(opts_row)

        btn_row = QHBoxLayout()
        self.btn_convert = QPushButton("Convert")
        self.btn_copy = QPushButton("Copy Output")
        self.btn_clear = QPushButton("Clear")
        btn_row.addWidget(self.btn_convert)
        btn_row.addWidget(self.btn_copy)
        btn_row.addWidget(self.btn_clear)
        btn_row.addStretch(1)
        layout.addLayout(btn_row)

        layout.addWidget(QLabel("Output:"))
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        mono = QFont("Courier New")
        mono.setStyleHint(QFont.Monospace)
        self.output.setFont(mono)
        layout.addWidget(self.output)

        self.btn_convert.clicked.connect(self.on_convert)
        self.btn_copy.clicked.connect(self.on_copy)
        self.btn_clear.clicked.connect(self.on_clear)

    def _convert_int_to_var(self, value: str) -> str:
        if _cli and hasattr(_cli, "integer_to_varint"):
            try:
                res = _cli.integer_to_varint(value, out=True) if "out" in _cli.integer_to_varint.__code__.co_varnames else _cli.integer_to_varint(value, True)
                if isinstance(res, (bytes, bytearray)):
                    return _hex_str(bytes(res), spaced=self.cb_hex_spaces.isChecked())
                if isinstance(res, (list, tuple)):
                    try:
                        return " ".join(str(x) for x in res)
                    except Exception:
                        return str(res)
                return str(res)
            except Exception as e:
                pass
        try:
            n = int(value, 0)
        except Exception:
            n = int(value)  
        b = _encode_varint_protobuf(n)
        return _hex_str(b, spaced=self.cb_hex_spaces.isChecked())

    def _convert_var_to_int(self, hex_str: str) -> str:
        data = _bytes_from_hex_str(hex_str)
        if _cli and hasattr(_cli, "varint_to_int"):
            try:
                res = _cli.varint_to_int(hex_str, out=True) if "out" in _cli.varint_to_int.__code__.co_varnames else _cli.varint_to_int(hex_str, True)
                return str(res)
            except Exception:
                pass
        val = _decode_varint_protobuf(data)
        return str(val)

    def on_convert(self):
        self.output.clear()
        text = self.input_edit.text().strip()
        if not text:
            QMessageBox.warning(self, "Input required", "Please enter a value to convert.")
            return
        try:
            if self.rb_int2var.isChecked():
                res = self._convert_int_to_var(text)
                self.output.setPlainText(res)
            else:
                res = self._convert_var_to_int(text)
                self.output.setPlainText(res)
        except Exception as e:
            QMessageBox.critical(self, "Conversion error", str(e))

    def on_copy(self):
        txt = self.output.toPlainText()
        if not txt:
            return
        cb: QClipboard = QApplication.clipboard()
        cb.setText(txt)

    def on_clear(self):
        self.input_edit.clear()
        self.output.clear()

def main():
    app = QApplication(sys.argv)
    w = VarintConverterGUI()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
