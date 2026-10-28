#!/usr/bin/env python3
"""
VDE Verification & Integrity Test Suite
Verifies all 12 native applications, compositor XMLs, Waybar JSONC, CSS, and installer
"""

import os
import sys
import py_compile
import xml.etree.ElementTree as ET
import json
import re

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_python_apps():
    print("[1/5] Verifying Python Application Syntax...")
    app_dirs = [
        "crossings/crossings_gui.py",
        "crosspad/crosspad.py",
        "crossminal/crossminal.py",
        "crossaint/crossaint.py",
        "crosstos/crosstos.py",
        "crossculator/crossculator.py",
        "crossmanager/crossmanager.py",
        "crosslock/crosslock.py",
        "crossbin/crossbin.py",
        "crossnarrator/crossnarrator.py",
        "crossnip/crossnip.py",
        "crosslink/crosslink.py"
    ]
    for rel_path in app_dirs:
        full_path = os.path.join(REPO_DIR, "apps", rel_path)
        assert os.path.exists(full_path), f"Missing: {full_path}"
        py_compile.compile(full_path, doraise=True)
        print(f"  [OK] {rel_path} syntax valid.")

    shell_scripts = [
        "astal-shell/vde_startmenu.py",
        "astal-shell/vde_quicksettings.py"
    ]
    for rel_path in shell_scripts:
        full_path = os.path.join(REPO_DIR, rel_path)
        assert os.path.exists(full_path), f"Missing: {full_path}"
        py_compile.compile(full_path, doraise=True)
        print(f"  [OK] {rel_path} syntax valid.")

def test_xml_configs():
    print("[2/5] Verifying Compositor XML Configurations...")
    xmls = ["compositor/rc.xml", "compositor/menu.xml"]
    for rel_path in xmls:
        full_path = os.path.join(REPO_DIR, rel_path)
        assert os.path.exists(full_path), f"Missing: {full_path}"
        ET.parse(full_path)
        print(f"  [OK] {rel_path} XML valid.")

def test_waybar_config():
    print("[3/5] Verifying Waybar JSONC Configuration...")
    wb_path = os.path.join(REPO_DIR, "astal-shell/waybar_config.jsonc")
    assert os.path.exists(wb_path), f"Missing: {wb_path}"
    with open(wb_path, "r", encoding="utf-8") as f:
        content = f.read()
    clean_json = re.sub(r'//.*', '', content)
    data = json.loads(clean_json)
    assert "modules-center" in data, "modules-center missing from Waybar config"
    assert "custom/start" in data["modules-center"], "custom/start missing"
    assert "wlr/taskbar" in data["modules-center"], "wlr/taskbar missing"
    print("  [OK] waybar_config.jsonc structure valid and verified.")

def test_desktop_files():
    print("[4/5] Verifying Desktop Entries...")
    apps_dir = os.path.join(REPO_DIR, "apps")
    count = 0
    for root, _, files in os.walk(apps_dir):
        for f in files:
            if f.endswith(".desktop"):
                fp = os.path.join(root, f)
                with open(fp, "r", encoding="utf-8") as df:
                    lines = df.readlines()
                assert any("[Desktop Entry]" in l for l in lines), f"Malformed: {f}"
                assert any(l.startswith("Exec=") for l in lines), f"Missing Exec=: {f}"
                assert any(l.startswith("Name=") for l in lines), f"Missing Name=: {f}"
                count += 1
                print(f"  [OK] {f} valid.")
    assert count >= 12, f"Expected at least 12 desktop entries, found {count}"

def test_installer_integrity():
    print("[5/5] Verifying install.sh Components...")
    inst_path = os.path.join(REPO_DIR, "install.sh")
    assert os.path.exists(inst_path), "install.sh missing"
    with open(inst_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "vde.service" in content, "vde.service missing from install.sh"
    assert "chvt 1" in content, "chvt 1 missing from install.sh"
    assert "trap '' HUP PIPE" in content, "Signal protection missing"
    print("  [OK] install.sh integrity checks passed.")

if __name__ == "__main__":
    test_python_apps()
    test_xml_configs()
    test_waybar_config()
    test_desktop_files()
    test_installer_integrity()
    print("\n[SUCCESS] ALL VDE STACK VERIFICATION TESTS PASSED (100% HEALTHY).")
