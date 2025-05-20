# EM Trace Acquisition Guide

## EM Signal Acquisition
To identify the optimal location for EM signal capture, multiple positions on the TOE were tested using probes of various shapes. The `Langer EMV RF-R 3-2` probe positioned at the location indicated in Figure below captured distinctive signals. These signals were closely correlated with the TOE's signature verification and firmware decryption operations.

<img src="./image/Probe.JPG" width="500"/>

## Oscilloscope Parameters

  |        Phase         | Sampling Rate | Bandwidth | Resolution | Duration | Vertical Resolution |
  | :------------------: | :-----------: | :-------: | :--------: | :------: | :-----------------: |
  | Preliminary Analysis |   250 MS/s    |  2.5 GHz  |   8-bit    | 18.5 ms  |    5 mV/division    |
  |   Real-World Attack   |    5 GS/s     |  2.5 GHz  |   8-bit    |  0.5 ms  |    5 mV/division    |

## Decryption Operations
Captured raw EM traces (18.5 ms @250 MS/s) were analyzed to identify the AES decryption window through distinct repetitive patterns. 
The red-marked segment (0.45 ms) in Figure below represents the firmware decryption process executed using the SBK. 
<img src="./image/EM_Trace_250M_SBK_Decryption.png" width="800"/>

