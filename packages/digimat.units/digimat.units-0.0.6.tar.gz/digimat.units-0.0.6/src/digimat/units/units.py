from prettytable import PrettyTable


class Units(object):

    UNIT_DIGITAL = 15
    UNIT_MULTISTATE = 53
    UNIT_HEX = 35
    UNIT_STR = ["V", "C", "Pa", "kPa", "%", "l/h", "bar", "Hz",
        "s", "ms", "min", "kW", "kWh", "J", "kJ", "",
        "m/s", "'", "h", "MWh", "MJ", "GJ", "W", "MW",
        "kJ/h", "MJ/h", "GJ/h", "ml", "l", "m3", "ml/h", "m3/h",
        "Wh", "?", "K", "", "lx", "t/min", "kVar", "kVarh",
        "mbar", "msg/m", "m", "kJ/kg", "g/kg", "ppm", "A", "kVA",
        "kVAh", "ohm", "", "mA", "mm", "", "W/m2"]

    def __init__(self):
        self._units={}
        self._indexByName={}
        for unit in range(len(self.UNIT_STR)):
            name=self.UNIT_STR[unit]
            self._units[unit]=name
            if name:
                self._indexByName[name.lower()]=unit

    def getByName(self, unit):
        try:
            return self._indexByName[unit.lower()]
        except:
            pass

    def getByNumber(self, unit):
        try:
            return self._units[int(unit)]
        except:
            pass

    def get(self, unit):
        unit=self.getByName(unit)
        if unit is None:
            unit=self.getByNumber(unit)
        return unit

    def str(self, unit):
        s=self.getByNumber(unit)
        return s or ''

    def __len__(self):
        return len(self.UNIT_STR)

    def __getitem__(self, key):
        return self.get(key)

    def __iter__(self):
        return iter(self._units.values())

    def isDigital(self, unit):
        try:
            if int(unit)==self.UNIT_DIGITAL:
                return True
        except:
            pass
        return False

    def digital(self):
        return self.UNIT_DIGITAL

    def multistate(self):
        return self.UNIT_MULTISTATE

    def none(self):
        return 0xFF

    def table(self, key=None):
        t=PrettyTable()
        t.field_names = ['#', 'unit']
        t.align['#']='l'
        t.align['unit']='l'
        for unit in range(len(self)):
            name=self.UNIT_STR[unit]
            if not key or key.lower() in name.lower():
                t.add_row([unit, name])
        print(t)

    def dump(self):
        for unit in range(len(self)):
            name=self.UNIT_STR[unit]
            print(unit, name)


# Empty = 0,            // pas de flags
# Alarm = 1,            // A [1] alarme
# AlarmAck = 2,         // K [2] alarme quitancée
# Warning = 4,          // W [4] avertissements
# Error = 8,            // E [8] erreur
# Manual = 0x10,        // M [16] manuel
# Derogation = 0x20,    // D [32] dérogation,
# Event = 0x40,         // V [64] événements
# Device = 0x80,        // X [128] propre au device
# Denied = 0x100,       // R [256] accès refusé
# Unknown = 0x200,      // U [512] ressource inconnue
# Timeout = 0x400,      // T [1024] time-out


class Flags(object):

    FLAGS = {'A': 1, 'K': 2, 'W': 4, 'E': 8, 'M': 16, 'D': 32, 'V': 64, 'X': 128, 'R': 256, 'U': 512, 'T': 1024}

    def __init__(self, flags=None):
        self._flags={}
        self.set(flags)

    def has(self, flags):
        if flags:
            for f in flags:
                if not self._flags.get(f.upper()):
                    return False
            return True
        return False

    def set(self, flags):
        if flags:
            for f in flags:
                f=f.upper()
                if f in self.FLAGS:
                    self._flags[f]=self.FLAGS[f]

    def flags(self):
        if self._flags:
            flags=''
            for f in self._flags.keys():
                flags+=f
            return flags

    def code(self):
        fcode=0
        if self._flags:
            for f in self._flags.values():
                fcode+=f
        return fcode

    def setError(self):
        self.set('E')

    @property
    def alarm(self):
        return self.has('A')

    @alarm.setter
    def alarm(self, value):
        self.set('E')

    @property
    def alarmack(self):
        return self.has('K')

    @alarmack.setter
    def alarmack(self, value):
        self.set('K')

    @property
    def warning(self):
        return self.has('W')

    @warning.setter
    def warning(self, value):
        self.set('W')

    @property
    def error(self):
        return self.has('E')

    @error.setter
    def error(self, value):
        self.set('E')

    @property
    def manual(self):
        return self.has('M')

    @manual.setter
    def manual(self, value):
        self.set('M')

    @property
    def derogation(self):
        return self.has('D')

    @derogation.setter
    def derogation(self, value):
        self.set('D')


if __name__=='__main__':
    pass
