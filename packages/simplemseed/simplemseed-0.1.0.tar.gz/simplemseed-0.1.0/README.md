# simplemseed


[![PyPI](https://img.shields.io/pypi/v/simplemseed)](https://pypi.org/project/simplemseed/)


[Miniseed3](http://docs.fdsn.org/projects/miniseed3) (and reading 2) in pure python

# Miniseed3

Read and write mseed3 records like:

```
#!/usr/bin/env python3

from simplemseed import MSeed3Header, MSeed3Record, FDSNSourceId, readMSeed3Records

data = [(i % 99 - 49) for i in range(0, 1000)]
header = MSeed3Header()
header.starttime = "2024-01-01T15:13:55.123456Z"
header.sampleRatePeriod = 20
sid = FDSNSourceId.createUnknown(header.sampleRatePeriod)
ms3record = MSeed3Record(header, sid, data)

ms3filename = "test.ms3"
with open(ms3filename, "wb") as of:
    of.write(ms3record.pack())
    print(f"  save: {ms3record.details()} ")
    print(f"    to: {ms3filename} ")
print()
with open(ms3filename, "rb") as infile:
    for readms3record in readMSeed3Records(infile):
        print(f"  extract: {readms3record.details()} ")
        print(f"     from: {ms3filename} ")
```

Access uncompressed timeseries data with:
```
dataArray = ms3record.decompress()
```


Also includes parsing for miniseed2 and
[miniseed3](http://docs.fdsn.org/projects/miniseed3/en/latest/index.html#) for primitive data arrays and
for Steim1 and Steim2 decompression, in pure python.

Read miniseed2:
```
with open(ms2filename, "rb") as inms2:
    for ms2rec in simplemseed.readMiniseed2Records(inms2):
        print(ms2rec.summary())
```
or read and convert to miniseed3:
```
with open(ms3filename, "wb") as outms3:
    with open(ms2filename, "rb") as inms2:
        for ms2rec in readMiniseed2Records(inms2):
            ms3rec = mseed2to3(ms2rec)
            outms3.write(ms3rec.pack())
```

# Command line tools:


#  mseed3details
- print details about each miniseed3 record
```
mseed3details casee.mseed3
          FDSN:CO_CASEE_00_H_H_Z, version 4, 285 bytes (format: 3)
                       start time: 2023-06-17T04:53:54.468392Z (168)
                number of samples: 104
                 sample rate (Hz): 100.0
                            flags: [00000000] 8 bits$
                              CRC: 0x4D467F27
              extra header length: 31 bytes
              data payload length: 192 bytes
                 payload encoding: STEIM-2 integer compression (val: 11)
                    extra headers:

Total 104 samples in 1 records
```

#  mseed3merge
- merge contiguous, in order, mseed3 records into larger records
```
mseed3merge -o co_merged.ms3 --decomp  co_feb6.ms3
```

#  mseed2to3
- convert miniseed 2 to miniseed3.

Note most blockettes are ignored, other than 100, 1000, 1001

```
mseed2to3 --ms2 casee.ms2 --ms3 casee.ms3
```


# fdsnsourceid
- parse FDSN sourceids

Split a FDSN source id:
```
fdsnsourceid FDSN:CO_JSC_00_H_H_Z
      FDSN:CO_JSC_00_H_H_Z
       Net: CO
       Sta: JSC
       Loc: 00
      Band: H - High Broadband, >= 80 to < 250 Hz, response period >= 10 sec
    Source: H - High Gain Seismometer
 Subsource: Z
```   

Describe a band code:
```
fdsnsourceid -b Q
      Band: Q - Q - Greater than 10 days , < 0.000001 Hz
```

Find the correct band code for a sample rate:
```
fdsnsourceid --sps 87
      Rate: 87.0 - H - H - High Broadband , >= 80 to < 250 Hz, response period >= 10 sec
      Rate: 87.0 - E - E - Extremely Short Period, >= 80 to < 250 Hz, response period < 10 sec
```

Describe a source code:
```
fdsnsourceid --source H N
    Source: H - High Gain Seismometer
       Measures displacement/velocity/acceleration along a line defined by the the dip and azimuth.
    Source: N - Accelerometer
       Measures displacement/velocity/acceleration along a line defined by the the dip and azimuth.
```

# Example

There are more examples in the examples directory.
