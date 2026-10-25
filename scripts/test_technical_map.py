import copy
import json
from pathlib import Path
import unittest
from build_technical_map import validate, render, verify_sources
import hashlib

class TechnicalMapTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((Path(__file__).resolve().parents[1]/'data/technical-map.json').read_text(encoding='utf-8'))
    def test_catalog_and_localized_outputs(self):
        validate(self.data)
        self.assertEqual(self.data['counts'], dict(areas=6, samples=12, connections=4, repositories=6, sourceFiles=24))
        self.assertEqual(len(self.data['areas']), 6)
        self.assertEqual(len(self.data['items']), 12)
        self.assertEqual(len(self.data['connections']), 4)
        self.assertEqual(len({e['repository'] for i in self.data['items'] for e in i['evidence']}), 6)
        self.assertEqual(sum(len(i['evidence']) for i in self.data['items']), 25)
        for lang in ('de','en','ru'):
            out=render(self.data,lang)
            self.assertIn('6 / 12',out)
            self.assertNotIn('{repositories}',out)
            for row in self.data['items']:
                self.assertEqual(out.count('<a id="'+row['id']+'"></a>'),1)
                for e in row['evidence']: self.assertIn(e['url'],out)
    def test_mutable_or_mismatched_source_link_is_rejected(self):
        for key,value in [('revision','main'),('url','https://example.invalid/'),('sha256','not-a-digest'),('startLine',0)]:
            sample=copy.deepcopy(self.data)
            sample['items'][0]['evidence'][0][key]=value
            with self.assertRaises(ValueError): validate(sample)
    def test_unsupported_runtime_promotion_is_rejected(self):
        self.data['items'][0]['review']='PRODUCTION_VERIFIED'
        with self.assertRaises(ValueError): validate(self.data)
    def test_missing_countercheck_or_translation_is_rejected(self):
        sample=copy.deepcopy(self.data)
        sample['items'][0]['evidence']=sample['items'][0]['evidence'][:1]
        with self.assertRaises(ValueError): validate(sample)
        del self.data['items'][0]['summary']['ru']
        with self.assertRaises(ValueError): validate(self.data)
    def test_unknown_cross_reference_is_rejected(self):
        self.data['connections'][0]['items'].append('invented-runtime')
        with self.assertRaises(ValueError): validate(self.data)

    def test_supplemental_urls_cannot_change_markdown_or_owner_binding(self):
        for kind in ('release', 'contribution'):
            # Synthetic valid links preserve both URL guards without retaining a
            # removed published sample or inventing a real release in the map.
            fixture = copy.deepcopy(self.data)
            route = 'releases/tag/fixture-v1.0.0' if kind == 'release' else 'commit/' + 'a' * 40
            original = 'https://github.com/Juri-Halveth/.github/' + route
            fixture['items'][0][kind] = dict(url=original)
            validate(fixture)
            for value in (original + ')\n\n[fixture](https://example.invalid/fixture', original + ' ', [original], 'https://github.com/Juri-Halveth/../commit/a', 'https://github.com/Juri-Halveth/./commit/a', 'https://github.com/Juri-Halveth/repo/commit/..'):
                sample = copy.deepcopy(fixture)
                sample['items'][0][kind]['url'] = value
                with self.assertRaisesRegex(ValueError, 'Invalid supplemental link'):
                    validate(sample)
        validate(self.data)

    def test_source_bytes_reject_a_well_formed_but_wrong_hash(self):
        payload = ('line\n' * 2000).encode('utf-8')
        sample = copy.deepcopy(self.data)
        for item in sample['items']:
            for evidence in item['evidence']:
                evidence['sha256'] = hashlib.sha256(payload).hexdigest()
        self.assertGreater(verify_sources(sample, lambda e: payload), 0)
        sample['items'][0]['evidence'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Source digest mismatch'):
            verify_sources(sample, lambda e: payload)

    def test_safe_release_tag_forms_and_dot_named_repository_remain_usable(self):
        for tag in ('release/v1.2.3', 'v1.2.3+build.1'):
            sample = copy.deepcopy(self.data)
            sample['items'][0]['release'] = dict(url='https://github.com/Juri-Halveth/.github/releases/tag/' + tag)
            validate(sample)

    def test_declared_counts_cannot_hide_removed_samples(self):
        for key in ('areas','samples','connections','repositories','sourceFiles'):
            sample = copy.deepcopy(self.data)
            sample['counts'][key] = 0
            with self.assertRaisesRegex(ValueError, 'Declared map counts'):
                validate(sample)
        sample = copy.deepcopy(self.data)
        sample['items'].pop()
        with self.assertRaisesRegex(ValueError, 'Declared map counts'):
            validate(sample)
        for lang in ('de','en','ru'):
            sample = copy.deepcopy(self.data)
            sample['introduction'][lang] = sample['introduction'][lang].replace('6 ', '7 ')
            with self.assertRaisesRegex(ValueError, 'actual repository count'):
                validate(sample)

    def test_empty_area_single_endpoint_or_duplicate_cross_reference_is_rejected(self):
        sample = copy.deepcopy(self.data)
        sample['areas'].append(dict(id='empty-topic', title=dict(de='Leer',en='Empty',ru='Пусто')))
        with self.assertRaisesRegex(ValueError, 'Empty area'):
            validate(sample)
        for endpoints in ([], self.data['connections'][0]['items'][:1],
                          self.data['connections'][0]['items'] * 2):
            sample = copy.deepcopy(self.data)
            sample['connections'][0]['items'] = endpoints
            with self.assertRaisesRegex(ValueError, 'distinct known endpoints'):
                validate(sample)
        sample = copy.deepcopy(self.data)
        sample['connections'][1]['id'] = sample['connections'][0]['id']
        with self.assertRaisesRegex(ValueError, 'Unique connection IDs'):
            validate(sample)

    def test_removed_presentation_cannot_return_through_catalog_or_evidence(self):
        for retired in ('Unreal', 'ashbound', 'morrowind', 'HALVETHRealms'):
            sample = copy.deepcopy(self.data)
            sample['items'][0]['summary']['en'] += ' Synthetic ' + retired
            with self.assertRaisesRegex(ValueError, 'Retired game presentation'):
                validate(sample)
        sample = copy.deepcopy(self.data)
        evidence = sample['items'][0]['evidence'][0]
        evidence['repository'] = 'Juri-Halveth/halveth-unreal'
        with self.assertRaisesRegex(ValueError, 'Retired game presentation'):
            validate(sample)

    def test_source_repository_cannot_escape_via_dot_only_segments(self):
        for repository in ('Juri-Halveth/.', 'Juri-Halveth/..'):
            sample = copy.deepcopy(self.data)
            evidence = sample['items'][0]['evidence'][0]
            evidence['repository'] = repository
            with self.assertRaisesRegex(ValueError, 'Public repository binding required'):
                validate(sample)

    def test_source_span_must_exist_in_actual_bytes(self):
        payload = b'one line\n'
        sample = copy.deepcopy(self.data)
        for item in sample['items']:
            for evidence in item['evidence']:
                evidence['sha256'] = hashlib.sha256(payload).hexdigest()
        with self.assertRaisesRegex(ValueError, 'Source span exceeds'):
            verify_sources(sample, lambda e: payload)

if __name__=='__main__': unittest.main()
