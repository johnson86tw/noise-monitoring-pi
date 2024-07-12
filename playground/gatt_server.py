import gatt

class CustomService(gatt.Service):
    UUID = '12345678-1234-5678-1234-56789abcdef0'

    def __init__(self, device):
        super().__init__(device)

    def characteristics(self):
        return [CustomCharacteristic(self)]

class CustomCharacteristic(gatt.Characteristic):
    UUID = '12345678-1234-5678-1234-56789abcdef1'

    def __init__(self, service):
        super().__init__(service, self.UUID, ["read"])

    def ReadValue(self, options):
        return [0x42]

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()
        print('Services resolved for device:', self.mac_address)

        custom_service = CustomService(self)
        self.add_service(custom_service)

class DeviceManager(gatt.DeviceManager):
    def device_discovered(self, device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))
        device.connect()

manager = DeviceManager(adapter_name='hci0')
manager.start_discovery()

try:
    manager.run()
except KeyboardInterrupt:
    manager.stop()