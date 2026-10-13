"""Split an already validated OCL export into concepts then mappings, without changing IDs."""
import argparse
import io
import json
import zipfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('source', type=Path)
p.add_argument('output', type=Path)
args = p.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
one = args.output / 'concepts.zip'
two = args.output / 'mappings.zip'
assert not one.exists() and not two.exists(), 'Refusing to overwrite phase archives'
decoder = json.JSONDecoder()
count = missing = duplicates = 0
uuids = set()
with zipfile.ZipFile(args.source) as source, \
        zipfile.ZipFile(one, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z1, \
        zipfile.ZipFile(two, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z2:
    assert source.testzip() is None, 'Source ZIP CRC failure'
    with io.TextIOWrapper(source.open('export.json'), encoding='utf8') as f, \
            z1.open('export.json', 'w', force_zip64=True) as o1, \
            z2.open('export.json', 'w', force_zip64=True) as o2:
        buf = f.read(65536)
        index = buf.find('"concepts":')
        assert index >= 0, 'Concepts field not found in export header'
        buf = buf[index + len('"concepts":'):].lstrip()
        assert buf.startswith('[')
        buf = buf[1:]
        o1.write(b'{"concepts":[')
        first = True
        while True:
            buf = buf.lstrip()
            if not buf:
                buf = f.read(65536)
                assert buf, 'Unexpected end of concepts array'
                continue
            if buf[0] == ']':
                o1.write(b'],"mappings":[]}')
                o2.write(b'{"concepts":[]')
                o2.write(buf[1:].encode())
                for chunk in iter(lambda: f.read(1048576), ''):
                    o2.write(chunk.encode())
                break
            try:
                concept, end = decoder.raw_decode(buf)
            except json.JSONDecodeError:
                more = f.read(65536)
                assert more, 'Truncated or invalid concept JSON'
                buf += more
                continue
            uuid = concept.get('external_id')
            if not uuid:
                missing += 1
            elif uuid in uuids:
                duplicates += 1
            else:
                uuids.add(uuid)
            o1.write(('' if first else ',').encode())
            o1.write(json.dumps(concept, ensure_ascii=False, separators=(',', ':')).encode())
            first = False
            count += 1
            buf = buf[end:].lstrip()
            if buf.startswith(','):
                buf = buf[1:]
assert missing == 0, 'Some concepts have no external ID; inspect before importing'
for archive in [one, two]:
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    assert archive.stat().st_size < 74990000, 'Phase archive exceeds OpenMRS upload limit'
(args.output / 'expected-concept-uuids.txt').write_text('\n'.join(sorted(uuids)) + '\n')
proof = {'concepts': count, 'unique_external_ids': len(uuids), 'duplicate_external_ids': duplicates,
         'zip_crc': 'OK', 'phases': [{'file': a.name, 'bytes': a.stat().st_size} for a in [one, two]]}
(args.output / 'phase-proof.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof))
