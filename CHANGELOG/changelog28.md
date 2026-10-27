# Changelog 28: Virtual Machine TCP Segmentation Offload (TSO) Network Optimization

## Summary
Resolved the 10-15 KB/s download bottleneck occurring in VirtualBox and virtual machine NAT environments:
1. **TCP Offload Bottleneck Elimination (`install.sh`)**:
   - Added automatic network adapter discovery and disabled TCP Segmentation Offload (`tso off`), Generic Segmentation Offload (`gso off`), and Generic Receive Offload (`gro off`).
   - Fixes packet fragmentation and dropped frames caused by VirtualBox's legacy Intel PRO/1000 (`82540EM`) NAT implementation, restoring full native network bandwidth.
2. **Persistence Explanation for Live Media**:
   - Clarified RAM-backed ephemeral nature of standard Live ISO sessions ("Try Ubuntu") and how to perform permanent installs vs instant session takeovers.
