# Measurement Setup Introduction
This File describes the hardware modifications and measurement setup necessary to minimize system noise and capture electromagnetic (EM) signals effectively. The goal is to improve the signal-to-noise ratio (SNR) for precise side-channel analysis of the NVIDIA Jetson Xavier NX SOM during firmware decryption. The EM measurement setup was designed to capture transient electromagnetic signals generated during the decryption of the MB1 firmware. The following components and configuration were used:
1. **Target of Evaluation (TOE)**: NVIDIA Jetson Xavier NX SOM, connected to a modified carrier board.

2. **Power Supplies**: Two Agilent E3631A DC power supplies provided clean 5V (VDD_IN) and 0.85V (VDD_CORE) inputs.

3. **Electromagnetic Probe**: A Langer EMV RF-R 3-2 probe was used to capture EM signals.

4. **RF Amplifier**: A Mini-Circuits ZFL-1000LN+ amplifier was used to amplify weak EM signals.

5. **Oscilloscope**: A Lecroy 625Zi oscilloscope recorded the amplified signals.

6. **Embedded Development Board**: A Jetson-based kit controlled the TOE's SYS_RESET pin and generated synchronized trigger signals for the oscilloscope.

<div style="text-align:center">
<img src="./image/setup.svg" alt="probe" style="zoom:10%; display: block; margin: 0 auto;" /></div>

## EM Signal Acquisition
The `Langer EMV RF-R 3-2` probe positioned at the location indicated in Figure captured distinctive signals. These signals were closely correlated with the TOE's signature verification and firmware decryption operations.

  |        Phase         | Sampling Rate | Bandwidth | Resolution | Duration | Vertical Resolution |
  | :------------------: | :-----------: | :-------: | :--------: | :------: | :-----------------: |
  | Preliminary Analysis |   250 MS/s    |  2.5 GHz  |   8-bit    | 18.5 ms  |    5 mV/division    |
  |   Real-World Attack   |    5 GS/s     |  2.5 GHz  |   8-bit    |  0.5 ms  |    5 mV/division    |

<div style="text-align:center">
<img src="./image/probe.JPG" alt="probe" style="zoom:10%; display: block; margin: 0 auto;" />
</div>
