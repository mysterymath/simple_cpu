EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 2
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	5050 2750 5600 2750
Connection ~ 5050 2750
Wire Wire Line
	5050 3000 5050 2750
Wire Wire Line
	4650 3000 5050 3000
$Comp
L Device:R R1
U 1 1 5E12BBE0
P 5050 2600
F 0 "R1" H 5120 2646 50  0000 L CNN
F 1 "10K" H 5120 2555 50  0000 L CNN
F 2 "" V 4980 2600 50  0001 C CNN
F 3 "~" H 5050 2600 50  0001 C CNN
	1    5050 2600
	1    0    0    -1  
$EndComp
$Comp
L simple_cpu:23x640 U3
U 1 1 5E0EE054
P 5900 2900
F 0 "U3" H 5750 3200 50  0000 C CNN
F 1 "23x640" H 6000 3200 50  0000 C CNN
F 2 "" H 5550 3100 50  0001 C CNN
F 3 "" H 5550 3100 50  0001 C CNN
	1    5900 2900
	1    0    0    -1  
$EndComp
Text HLabel 6250 2950 2    50   Input ~ 0
SCLK
Text HLabel 6250 3050 2    50   Input ~ 0
SIO
Text HLabel 5600 2850 0    50   Input ~ 0
SIO
Connection ~ 5050 4050
$Comp
L Device:R R2
U 1 1 5E12CC57
P 5050 3900
F 0 "R2" H 5120 3946 50  0000 L CNN
F 1 "10K" H 5120 3855 50  0000 L CNN
F 2 "" V 4980 3900 50  0001 C CNN
F 3 "~" H 5050 3900 50  0001 C CNN
	1    5050 3900
	1    0    0    -1  
$EndComp
$Comp
L Memory_EEPROM:25LCxxx U4
U 1 1 5E115D54
P 5950 4050
F 0 "U4" H 5700 4300 50  0000 C CNN
F 1 "25LC010A" H 6150 4300 50  0000 C CNN
F 2 "" H 5950 4050 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/21832H.pdf" H 5950 4050 50  0001 C CNN
	1    5950 4050
	1    0    0    -1  
$EndComp
Text HLabel 5550 4150 0    50   Input ~ 0
B~CS~
Wire Wire Line
	5050 4050 5550 4050
Wire Wire Line
	5050 4150 5050 4050
Wire Wire Line
	4600 4150 5050 4150
$Comp
L Memory_EEPROM:25LCxxx U1
U 1 1 5E11FF97
P 4200 4050
F 0 "U1" H 3950 4300 50  0000 C CNN
F 1 "25LC010A" H 4400 4300 50  0000 C CNN
F 2 "" H 4200 4050 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/21832H.pdf" H 4200 4050 50  0001 C CNN
	1    4200 4050
	1    0    0    -1  
$EndComp
Text HLabel 4600 4050 2    50   Input ~ 0
BSI
Text HLabel 3800 4150 0    50   Input ~ 0
B~CS~
Text HLabel 4600 3950 2    50   Input ~ 0
HCLK
Text HLabel 6350 4150 2    50   Input ~ 0
SIO
Text HLabel 6350 4050 2    50   Input ~ 0
BSI
Text HLabel 6350 3950 2    50   Input ~ 0
SCLK
Text HLabel 4650 2900 2    50   Input ~ 0
BSI
Text HLabel 4650 2800 2    50   Input ~ 0
SCLK
Text HLabel 3850 3000 0    50   Input ~ 0
B~CS~
$Comp
L Memory_EEPROM:25LCxxx U5
U 1 1 5E103051
P 5050 4850
F 0 "U5" H 4800 5100 50  0000 C CNN
F 1 "25LC010A" H 5250 5100 50  0000 C CNN
F 2 "" H 5050 4850 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/21832H.pdf" H 5050 4850 50  0001 C CNN
	1    5050 4850
	1    0    0    -1  
$EndComp
Text HLabel 5450 4850 2    50   Input ~ 0
BSI
Text HLabel 4650 4950 0    50   Input ~ 0
B~CS~
Text HLabel 5450 4750 2    50   Input ~ 0
SCLK
Text HLabel 5450 4950 2    50   Input ~ 0
~CS~
Text HLabel 4250 2600 1    50   Input ~ 0
Vcc
Text HLabel 5050 2450 1    50   Input ~ 0
Vcc
Text HLabel 6250 2750 2    50   Input ~ 0
Vcc
Text HLabel 5050 3750 1    50   Input ~ 0
Vcc
Text HLabel 4200 3750 1    50   Input ~ 0
Vcc
Text HLabel 3850 2900 0    50   Input ~ 0
Vcc
Text HLabel 3800 4050 0    50   Input ~ 0
Vcc
Text HLabel 4650 4850 0    50   Input ~ 0
Vcc
$Comp
L Memory_EEPROM:25LCxxx U2
U 1 1 5E0E5B69
P 4250 2900
F 0 "U2" H 4000 3150 50  0000 C CNN
F 1 "25LC010A" H 4450 3150 50  0000 C CNN
F 2 "" H 4250 2900 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/21832H.pdf" H 4250 2900 50  0001 C CNN
	1    4250 2900
	1    0    0    -1  
$EndComp
Text HLabel 3850 2800 0    50   Input ~ 0
Vss
Text HLabel 5600 3050 0    50   Input ~ 0
Vss
Text HLabel 3800 3950 0    50   Input ~ 0
Vss
Text HLabel 5550 3950 0    50   Input ~ 0
Vss
Text HLabel 4650 4750 0    50   Input ~ 0
Vss
Text HLabel 4200 4350 3    50   Input ~ 0
Vss
Text HLabel 5950 4350 3    50   Input ~ 0
Vss
Text HLabel 5050 5150 3    50   Input ~ 0
Vss
Text HLabel 5950 3750 1    50   Input ~ 0
Vcc
Text HLabel 5050 4550 1    50   Input ~ 0
Vcc
Text HLabel 6250 2850 2    50   Input ~ 0
Vcc
$EndSCHEMATC