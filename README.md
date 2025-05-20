# Fight-Fire-with-Fire-Attack
This repository contains the artifact for our paper "**Classical Attacks, Modern Targets:Side-Channel Compromises Secure Boot Key in NVIDIA Jetson Edge AI**" published at NDSS 2026.

Our investigation uncovered **Fight-Fire-with-Fire Attack**, a novel and unpatchable vulnerability in the Nvidia Jetson Xavier NX SoC, which enabling `Secure Boot key (SBK)` and `Nvidia's MB1 Encryption Key (NV-MEK)` recovery through GPU-accelerated 32-bit correlation power analysis (CPA) within 10 hours.

This vulnerability has been reproduced and acknowledged by NVIDIA. In accordance with lawful vulnerability disclosure protocols, it has been assigned the CVE identifier **CVE-2025-286543**, and mitigation measures have been published. 

For details, refer to: <https://www.nvidiasecurity.com>

## Structure Descriptions
This repository is structured as follows:
- **`EM_Trace_Acquisition`**: Contains contains a guide for electromagnetic (EM) trace acquisition during the decryption of the MB1 firmware with SBK.

- **`Hardware_Setup`**: Contains the hardware setup guide for the electromagnetic (EM) acquisition framework, which enables efficient and low-noise electromagnetic (EM) signal acquisition. 

- **`Proof_of_Concept`**: Contains all scripts, CUDA code, and electromagnetic (EM) trace datasets required to complete the Proof of Concept (PoC) validation.
  - **Notes**
    - **OS Requirements**: Linux x86-64
    - **Docker Image**: <nvcr.io/nvidia/cuda:12.1.1-devel-ubuntu22.04> 
    - **Python Version**: ≥ 3.8
    - **GPU Requirements**: 4 x Nvidia GPU
