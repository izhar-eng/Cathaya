"""Import ordered local OCL ZIPs, checking each result before the next phase."""
import argparse
import base64
import json
import subprocess
import time
import urllib.request
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--work', type=Path, required=True)
p.add_argument('--status', type=Path, required=True)
p.add_argument('--prefix', default='carthaya-restore')
p.add_argument('--engine', default='colima-r')
p.add_argument('archives', type=Path, nargs='+')
args = p.parse_args()
values = dict(line.split('=', 1) for line in (args.repo / '.env').read_text().splitlines()
              if '=' in line and not line.startswith('#'))
auth = 'Basic ' + base64.b64encode(('admin:' + values['CARTHAYA_ADMIN_PASSWORD']).encode()).decode()

def sql(query):
    command = ['docker', 'exec', '-i', args.prefix + '-db-1', 'sh', '-c',
               'export MYSQL_PWD="$MARIADB_ROOT_PASSWORD"; exec mariadb --user=root --batch --skip-column-names "$MARIADB_DATABASE"']
    return subprocess.check_output(command, input=query, text=True, timeout=30).strip()

def api(path):
    request = urllib.request.Request('http://127.0.0.1:8080/openmrs/ws/rest/v1/' + path,
                                    headers={'Authorization': auth})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)

state = {'version': 'v2026-09-24', 'state': 'preparing', 'completed_phases': []}

def report():
    state['updated_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    text = json.dumps(state, ensure_ascii=False, indent=2) + '\n'
    temp = args.work / 'progress.tmp'
    temp.write_text(text)
    temp.replace(args.work / 'progress.json')
    args.status.write_text('Carthaya — installation CIEL\n\n' + text)
    print(json.dumps(state), flush=True)

def latest():
    row = sql("SELECT JSON_OBJECT('id',import_id,'uuid',uuid,'started',local_date_started,'stopped',local_date_stopped,'has_error',error_message IS NOT NULL) FROM openconceptlab_import ORDER BY import_id DESC LIMIT 1;")
    return json.loads(row) if row else {'id': 0, 'stopped': True}

try:
    assert subprocess.check_output(['docker', 'info', '--format', '{{.Name}}'], text=True).strip() == args.engine
    assert (args.work / 'archive-proof.json').exists(), 'Backup proof required'
    assert not (args.work / 'phases-started.json').exists(), 'A run was already initiated; inspect it before retrying'
    assert all(archive.stat().st_size < 74990000 for archive in args.archives)
    current = latest()
    assert current['stopped'], 'An import is already running'
    patient_count = int(sql('SELECT COUNT(*) FROM patient;'))
    patient_uuid = sql('SELECT p.uuid FROM person p JOIN patient t ON t.patient_id=p.person_id LIMIT 1;')
    (args.work / 'phases-started.json').write_text(json.dumps({'baseline_import_id': current['id'], 'archives': [a.name for a in args.archives]}))
    for index, archive in enumerate(args.archives, 1):
        state.update({'state': 'uploading', 'phase': index, 'phases': len(args.archives), 'archive': archive.name})
        report()
        baseline = latest()['id']
        remote_file = '/tmp/carthaya-ciel-phase-' + str(index) + '.zip'
        subprocess.run(['docker', 'cp', str(archive), args.prefix + '-backend-1:' + remote_file], check=True, capture_output=True, timeout=120)
        config = 'header = "Authorization: ' + auth + '"\n'
        response = subprocess.run(['docker', 'exec', '-i', args.prefix + '-backend-1', 'curl', '--silent', '--show-error', '--max-time', '180', '--config', '-',
                                   '--form', 'file=@' + remote_file + ';type=application/zip', '--write-out', '\n%{http_code}',
                                   'http://127.0.0.1:8080/openmrs/ws/rest/v1/openconceptlab/import'], input=config, text=True, capture_output=True, timeout=200)
        body, code = response.stdout.rsplit('\n', 1)
        assert response.returncode == 0 and code in ['200', '201'], 'Upload failed; inspect server logs and import state, do not automatically retry'
        state['upload_http'] = int(code)
        state['state'] = 'running'
        for _ in range(1440):
            current = latest()
            state['import'] = current
            state['concepts'] = int(sql('SELECT COUNT(*) FROM concept;'))
            if current['id'] > baseline:
                state['processed_items'] = int(sql('SELECT COUNT(*) FROM openconceptlab_item WHERE import_id=' + str(current['id']) + ';'))
                if current['stopped']:
                    detail = api('openconceptlab/import/' + current['uuid'] + '?v=full')
                    assert not current['has_error'] and detail.get('errorItemsCount') == 0, 'Import completed with errors; next phase withheld'
                    state['completed_phases'].append({'phase': index, 'uuid': current['uuid'], 'items': detail.get('allItemsCount'), 'errors': detail.get('errorItemsCount')})
                    break
            report()
            time.sleep(30)
        else:
            raise TimeoutError('Monitoring window ended; inspect running import')
        report()
    expected = set((args.work / 'expected-concept-uuids.txt').read_text().splitlines())
    present = set(sql('SELECT uuid FROM concept;').splitlines())
    state['expected_unique_concepts'] = len(expected)
    state['missing_concepts'] = len(expected - present)
    assert state['missing_concepts'] == 0, 'Expected CIEL concepts are missing'
    state['authenticated'] = bool(api('session').get('authenticated'))
    state['patients'] = int(sql('SELECT COUNT(*) FROM patient;'))
    state['patient_preserved'] = state['patients'] == patient_count and api('patient/' + patient_uuid).get('uuid') == patient_uuid
    state['search_counts'] = {term: len(api('concept?q=' + term).get('results', [])) for term in ['diabetes', 'malaria', 'hypertension']}
    assert state['authenticated'] and state['patient_preserved'], 'Post-import application validation failed'
    assert all(state['search_counts'].values()), 'Clinical search returned no results'
    state['state'] = 'validated'
    report()
except Exception as error:
    state['state'] = 'needs-review'
    message = str(error)
    for secret in values.values():
        if secret:
            message = message.replace(secret, '[REDACTED]')
    state['error'] = type(error).__name__ + ': ' + message[:300]
    report()
    raise SystemExit(1)
