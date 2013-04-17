from nswrapper import netsnmp

class OidDoesNotExists(Exception):
    pass

class SnmpDataType(object):
    
    VALUE_TYPE = str
    VARBIND_TYPE = ''
    
    class DoesNotExists(Exception):
        pass
    
    def __init__(self, oid, value=None, iid=None):
        self.oid = oid
        self.iid = iid
        self.value = self.validate(value)
    
    def validate(self, value):
        """Format and validate varbind value
        """
        value = self.VALUE_TYPE(value) if not value == None else None
        return value
    
    def __unicode__(self):
        """Represent the unicode value
        """
        return str(self.value)
    
    def varbind_value(self):
        """
        Like __unicode__, but format result for the \
        netsnmp.Varbind.val property
        """
        return str(self.value)
    
    def get_varbind(self):
        """ Convert the datatype to a netsnmp.Varbind object
        """
        varbind = netsnmp.Varbind(self.oid)
        varbind.iid = self.iid
        varbind.type = self.TYPE
        varbind.val = self.__unicode__()
        return varbind


class ObjectId(SnmpDataType):
    VARBIND_TYPE = 'OBJECTID'

class OctetStr(SnmpDataType):
    VARBIND_TYPE = 'OCTETSTR'

class Integer(SnmpDataType):
    VARBIND_TYPE = 'INTEGER'

class NetAddr(SnmpDataType):
    VARBIND_TYPE = 'NETADDR'

class IpAddr(SnmpDataType):
    VARBIND_TYPE = 'IPADDR'

class Counter(SnmpDataType):
    VARBIND_TYPE = 'COUNTER'
    VALUE_TYPE = int

class Counter64(SnmpDataType):
    VARBIND_TYPE = 'COUNTER64'
    VALUE_TYPE = int

class Gauge(SnmpDataType):
    VARBIND_TYPE = 'GAUGE'
    VALUE_TYPE = int

class UInteger(SnmpDataType):
    VARBIND_TYPE = 'UINTEGER'
    VALUE_TYPE = int

class Ticks(SnmpDataType):
    VARBIND_TYPE = 'TICKS'
    VALUE_TYPE = float
    
    def validate(self, value):
        from datetime import datetime
        value = super(Ticks, self).validate(value)
        if not isinstance(value, datetime):
            value = datetime.fromtimestamp(value)
        return value
    
    def varbind_value(self):
        return str(self.value.strftime("%s"))


class Opaque(SnmpDataType):
    VARBIND_TYPE = 'OPAQUE'

class Null(SnmpDataType):
    VARBIND_TYPE = 'NULL'
    
    def validate(self, value):
        return None
    
    def __unicode__(self):
        return ""

class NoSuchInstance(SnmpDataType):
    def __init__(self, oid, *args, **kwargs):
        m = "oid %s does not exists" % oid
        raise self.DoesNotExists(m)


TYPESMAP = {'OBJECTID': ObjectId,
            'OCTETSTR': OctetStr,
            'INTEGER': Integer,
            'NETADDR': NetAddr,
            'IPADDR': IpAddr,
            'COUNTER': Counter,
            'COUNTER64': Counter64,
            'GAUGE': Gauge,
            'UINTEGER': UInteger,
            'TICKS': Ticks,
            'OPAQUE': Opaque,
            'NULL': Null,
            'NOSUCHINSTANCE': NoSuchInstance}

def get_datatype(varbind):
    if not isinstance(varbind, netsnmp.Varbind):
        raise TypeError("netsnmp.Varbind expected")
    
    try:
        Cls = TYPESMAP[varbind.type]
        return Cls(varbind.tag,value=varbind.val,iid=varbind.iid)
    except KeyError:
        m = "DataType %s does not exists" % varbind.type
        raise OidDoesNotExists(m)
    except:
        raise
