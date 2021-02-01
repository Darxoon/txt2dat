# txt2dat
Converts semi-machine-readable key-pair hash data into a machine-readable xml ROM datfile snippit.


e.g.
```shell
$ txt2dat
CRC32: a
md5: B
sha-256: c
sha1: d
size: 123456

or

```shell
$ cat hashes.txt | txt2dat
```

outputs

```shell
<game><rom size="123456" crc="A" md5="B" sha1="D" sha256="C" /></game>
```

As you can see, it can cope with somewhat inconsistent formatting.

## Todo

* Code needs refactoring
* Add checks for correct length and characters in size and hashes
* Warn on missing fields
