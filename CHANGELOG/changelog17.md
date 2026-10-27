# Changelog 17: Fix Batch Parser Conflict in QEMU Launcher

## Summary
Resolved a batch script parsing conflict in `Launch_VDE_QEMU.bat` where nested parentheses inside conditional blocks caused Windows `cmd.exe` to abort with a syntax error upon user selection.

## Root Cause Analysis
In Windows command script (`.bat`) syntax, parentheses inside nested `if (...) else (...)` blocks and multi-line caret (`^`) statements prematurely terminate the block parser. When the user entered `1` and pressed Enter, the shell encountered an unbalanced parenthesis, raised `... was unexpected at this time`, and terminated the terminal window before QEMU could be dispatched.

## Key Changes
1. **Refactored Batch Flow (`Launch_VDE_QEMU.bat`)**:
   - Replaced parenthesized conditional blocks with explicit label branching (`goto use_tryout` / `goto use_server`).
   - Removed nested parentheses from output text and eliminated accidental stream redirection operators.
   - Formatted the QEMU launch command onto a clean, single-line invocation to ensure robust cross-shell execution.
