# Changelog 43: Repository Namespace Migration to i2qq & Single-Command URL Updates

## Summary
Migrated repository namespace and installer endpoints following repository ownership transfer to `i2qq`:

1. **Remote Endpoint Migration**:
   - Updated primary git remote URL to `https://github.com/i2qq/VDE.git`.
   - Updated `install.sh` download sources and SHA-256 package retrieval to `https://github.com/i2qq/VDE/archive/refs/heads/main.tar.gz`.
2. **Short Universal Installer Command**:
   - Updated documentation and scripts to the concise 4-character handle URL:
     ```bash
     wget -qO- https://raw.githubusercontent.com/i2qq/VDE/main/install.sh | sudo bash
     ```
3. **Application Verification Payload**:
   - Confirmed all 12 core native applications (Crossings, Crosspad, Crossminal, Crossaint, Crosstos, Crossculator, Crossmanager, Crosslock, Cross Bin, Cross Narrator, Crossnip, Crosslink) are packaged and deployed under the new repository namespace.
