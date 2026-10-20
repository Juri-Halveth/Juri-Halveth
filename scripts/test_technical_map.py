import copy
import json
from pathlib import Path
import unittest
from build_technical_map import validate, render

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

if __name__=='__main__': unittest.main()
