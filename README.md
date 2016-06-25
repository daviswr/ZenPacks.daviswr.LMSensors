# ZenPacks.daviswr.LMSensors

ZenPack to model & monitor fans, voltages, and temperature sensors on a Linux system with sensord via LM-SENSORS-MIB

## Usage

This ZenPack overrides the Fan, PowerSupply, and TemperatureSensor monitoring templates at the /Server/Linux device class, but doesn't (yet) modify the modeler plugins configured there, so it's up to you to apply the `daviswr.snmp.LMSensors*Map` modelers.
