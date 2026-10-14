"""Prepare a small, audited OCL retry without truncating clinical labels."""
import argparse
import copy
import json
import uuid
import zipfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('rejected', type=Path, help='JSON array of original rejected OCL concepts')
p.add_argument('output', type=Path)
p.add_argument('--synonym-name', action='append', default=[], help='External name ID to demote from preferred/fully specified to synonym')
args = p.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
destination = args.output / 'concepts-repaired.zip'
assert not destination.exists(), 'Refusing to overwrite repair package'
original = json.loads(args.rejected.read_text())
concepts = copy.deepcopy(original)
audit = []
seen_synonyms = set()
for concept in concepts:
    kept = []
    for name in concept.get('names', []):
        text = name.get('name') or ''
        if len(text) > 255:
            description_id = str(uuid.uuid5(uuid.NAMESPACE_URL, concept['url'] + '/carthaya/preserved-name/' + name['external_id']))
            description = {'uuid': description_id, 'external_id': description_id,
                           'type': 'ConceptDescription', 'description': text,
                           'locale': name['locale'], 'locale_preferred': False,
                           'description_type': None, 'retired': False}
            concept.setdefault('descriptions', []).append(description)
            audit.append({'concept_id': concept['id'], 'concept_uuid': concept['external_id'],
                          'action': 'preserve_overlong_name_in_description', 'original_name': copy.deepcopy(name),
                          'description_uuid': description_id})
            continue
        if name.get('external_id') in args.synonym_name:
            before = copy.deepcopy(name)
            name['name'] = text.strip()
            name['name_type'] = None
            name['locale_preferred'] = False
            seen_synonyms.add(name['external_id'])
            audit.append({'concept_id': concept['id'], 'concept_uuid': concept['external_id'],
                          'action': 'demote_duplicate_to_synonym', 'original_name': before,
                          'updated_name': copy.deepcopy(name)})
        kept.append(name)
    concept['names'] = kept
    assert any(n.get('name_type') == 'FULLY_SPECIFIED' and not n.get('retired') for n in kept), 'No remaining active fully specified name'
    assert all(0 < len(n['name']) <= 255 for n in kept)
assert seen_synonyms == set(args.synonym_name), 'Requested synonym name ID not found'
assert [(c['id'], c['external_id'], c['url']) for c in concepts] == [(c['id'], c['external_id'], c['url']) for c in original]
with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr('export.json', json.dumps({'concepts': concepts, 'mappings': []}, ensure_ascii=False))
with zipfile.ZipFile(destination) as z:
    assert z.testzip() is None
    assert len(json.loads(z.read('export.json'))['concepts']) == len(original)
(args.output / 'repair-audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'concepts': len(concepts), 'preserved_long_labels': sum(a['action'] == 'preserve_overlong_name_in_description' for a in audit),
                  'synonym_changes': len(seen_synonyms), 'concept_ids_unchanged': True, 'zip_crc': 'OK'}))
