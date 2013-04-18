Nswrapper provide an abstraction layer to the netsnmp python bindings:


<pre>
<code>
Python 2.7.3 (default, Sep 26 2012, 21:51:14) 
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.

>>> #! /usr/bin/python
>>> import nswrapper
 

>>> # Initialize session
>>> snmp = nswrapper.Snmp(host='localhost')

>>> # Getting system information
>>> data = snmp.get(".1.3.6.1.2.1.1.1.0").next()
>>> print data  
Linux pc-local 3.5.0-27-generic #46-Ubuntu SMP Mon Mar 25 19:58:17 UTC 2013 x86_64

>>> print data.value  
Linux pc-local 3.5.0-27-generic #46-Ubuntu SMP Mon Mar 25 19:58:17 UTC 2013 x86_64

>>> print type(data)  
&lt;class 'nswrapper.types.OctetStr'&gt;

>>> print type(data.value)
&lt;type 'str'&gt;

>>> print data.oid  
iso.3.6.1.2.1.1.1.0

>>> for data in snmp.get(".1.3.6.1.2.1.1.1.0", ".1.3.6.1.2.1.1.2.0"):
...     print data.oid + " - " + data.value
iso.3.6.1.2.1.1.1.0 - Linux pc-guillaume 3.5.0-27-generic #46-Ubuntu SMP Mon Mar 25 19:58:17 UTC 2013 x86_64
iso.3.6.1.2.1.1.2.0 - .1.3.6.1.4.1.8072.3.2.10
</code>
</pre>

See the api reference in the wiki for more informations.
