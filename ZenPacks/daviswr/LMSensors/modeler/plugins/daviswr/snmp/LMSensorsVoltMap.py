__doc__ = """LMSensorsVoltMap

maps SNMP voltage information onto PowerSupply components

"""

from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetTableMap

class LMSensorsVoltMap(SnmpPlugin):
    maptype = 'PowerSupply'
    compname = 'hw'
    relname = 'powersupplies'
    modname = 'Products.ZenModel.PowerSupply'

    snmpGetTableMaps = (
        GetTableMap('lmVoltSensorsEntry', '.1.3.6.1.4.1.2021.13.16.4.1',
            {
                '.2': 'lmVoltSensorsDevice',
            }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        log.debug("%s tabledata = %s", device.id, tabledata)

        sensorsTable = tabledata.get('lmVoltSensorsEntry')
        if sensorsTable is None:
            log.error('Unable to get data for %s for lmVoltSensorsTable' % device.id)
            return None

        rm = self.relMap()

        for snmpindex, row in sensorsTable.items():
            id = row.get('lmVoltSensorsDevice', '')
            om = self.objectMap(row)
            om.snmpindex  = snmpindex.strip('.')
            om.id = self.prepId(id)
            # Should ignore low, high, crit, and hyst values
            if self.hasThreshold(om, rm):
                continue
            rm.append(om)

        log.debug('%s relMap %s', device.id, rm)
        return rm

    def hasThreshold(self, om, rm):
        for map in rm:
            if map.id == om.id:
                if int(map.snmpindex) > int(om.snmpindex):
                    # Replace the existing entry's higher SNMP index
                    map.snmpindex = om.snmpindex
                return True
        return False
