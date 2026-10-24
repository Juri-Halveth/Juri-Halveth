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
        for lang in ('de','en','ru'):
            out=render(self.data,lang)
            for row in self.data['items']:
                self.assertIn('id="'+row['id']+'"',out)
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
            target = next(i for i in self.data['items'] if kind in i)
            original = target[kind]['url']
            for value in (original + ')\n\n[fixture](https://example.invalid/fixture', original + ' ', [original], 'https://github.com/Juri-Halveth/../commit/a', 'https://github.com/Juri-Halveth/./commit/a', 'https://github.com/Juri-Halveth/repo/commit/..'):
                sample = copy.deepcopy(self.data)
                next(i for i in sample['items'] if kind in i)[kind]['url'] = value
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
            next(i for i in sample['items'] if 'release' in i)['release']['url'] = 'https://github.com/Juri-Halveth/.github/releases/tag/' + tag
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
