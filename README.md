## Table of Contents
1. [Introduction](#introduction)
2. [Hardware Setup](#hardware-setup)
    1. [Raspberry Pi 4B](#rasperry-pi-4b)
    2. [RC522](#rc522)


## Introduction

Radio Frequency Identification (RFID) systems consist of three components: *tags* also known as labels or transponders [2], *readers* also known as interrogators [2] and a back-end server [1]. RFID systems are used to track tags attached to objects through space and time and have thus found applications in a wide range of fields [3].

## Hardware Setup

### Raspberry Pi 4B

A Raspberry Pi 4B (RPi4b) with Rapsbian installed was used for this project.

#### Pin Diagram

The pin diagram of the RPi4b can be generated by running the command `gpio readall`.

    $ gpio readall

##### Output

    +-----+-----+---------+------+---+---Pi 4B--+---+------+---------+-----+-----+
    | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
    +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
    |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
    |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5v      |     |     |
    |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
    |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | IN   | TxD     | 15  | 14  |
    |     |     |      0v |      |   |  9 || 10 | 1 | IN   | RxD     | 16  | 15  |
    |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
    |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
    |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
    |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
    |  10 |  12 |    MOSI | ALT0 | 0 | 19 || 20 |   |      | 0v      |     |     |
    |   9 |  13 |    MISO | ALT0 | 0 | 21 || 22 | 1 | IN   | GPIO. 6 | 6   | 25  |
    |  11 |  14 |    SCLK | ALT0 | 0 | 23 || 24 | 1 | OUT  | CE0     | 10  | 8   |
    |     |     |      0v |      |   | 25 || 26 | 1 | OUT  | CE1     | 11  | 7   |
    |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
    |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
    |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
    |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
    |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
    |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
    |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
    +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
    | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
    +-----+-----+---------+------+---+---Pi 4B--+---+------+---------+-----+-----+

>Warning: This command only works for `gpio` versions `>=2.52`.

### RC522

A RC522 `13.56MHz` RFID module is used as the receiver. This module is based on the MFRC522 IC (integrated circuit) released by NXP Semiconductors. The RPi4b and RC522 communicate using a Serial Peripheral Interface (SPI). The RC522 module is wired up with the help of the RPi4b [pin diagram](#output) above. 

## Access Control System

In order to showcase the usefulness of RFID systems, this project presents an RFID based control system

### System Overview

### Functional Requirements

### Non-functional Requirements

## Limitations

## Conclusion

## References

1. Chen, Y.Y. and Tsai, M.L., "The Study on Secure RFID Authentication and Access Control", Current Trends and Challenges in RFID, p.393, 2011.

2. EPCglobal, G.S., "EPC Radio-Frequency Identity Protocols Generation-2 UHF RFID; Specification for RFID Air Interface Protocol for Communications at 860 MHz –960 MHz", EPCglobal Inc., November 2013.

3. Sethi G, Dharani A., "Challenges of Radio Frequency Identification Technique.", International Journal of Science and Research (IJSR), https://www.ijsr.net/search_index_results_paperid.php?id=OCT14721, Volume 3, Issue 11, pp. 51 - 55, November 2014. 