import pathlib,tempfile,unittest,zipfile
from survey_datfiles import Stats,parse_dat,survey,timestamp
H='a'*40
class SurveyTests(unittest.TestCase):
 def test_same_size_and_hash_only(self):
  s=Stats()
  for size in (16,16,32):s.rom({'name':'x.bin','size':str(size),'sha1':H})
  r=s.report();self.assertEqual(r['repeated_file_bytes'],16);self.assertEqual(r['unique_file_identities'],2)
 def test_missing_hash_and_nodump_are_not_savings(self):
  s=Stats();s.rom({'name':'x','size':'16','crc':'12345678'});s.rom({'name':'y','size':'16','sha1':H,'status':'nodump'})
  self.assertEqual(s.report()['eligible_rom_bytes'],0);self.assertIsNone(s.report()['repeated_file_percent'])
 def test_bad_dump_remains_a_declared_identity(self):
  s=Stats();s.rom({'name':'x','size':'16','sha1':H,'status':'baddump'})
  self.assertEqual(s.report()['unique_file_bytes'],16);self.assertEqual(s.report()['statuses']['baddump'],1)
 def test_chd_disk_hash_domain_is_separate(self):
  s=Stats();s.disk({'sha1':H});s.disk({'sha1':H});s.rom({'name':'a.chd','size':'16','sha1':H})
  r=s.report();self.assertEqual(r['disk_records'],2);self.assertEqual(r['unique_disk_sha1'],1);self.assertEqual(r['repeated_file_bytes'],0)
 def test_cue_descriptor_excluded_from_media_estimate(self):
  s=Stats()
  for _ in range(2):s.rom({'name':'x.cue','size':'16','sha1':H})
  self.assertEqual(s.report()['repeated_file_bytes'],16);self.assertEqual(s.report()['eligible_media_bytes'],0)
 def test_parser_counts_relations_without_expanding_them(self):
  xml=f'<datafile><header><name>Test</name></header><machine name="c" cloneof="p" romof="bios"><device_ref name="dev"/><rom name="x" size="16" sha1="{H}" merge="base"/></machine></datafile>'.encode()
  header,s=parse_dat(xml);r=s.report();self.assertEqual(header['name'],'Test');self.assertEqual([r[k] for k in ('sets','cloneof','romof','device_ref','rom_merge_attributes')],[1]*5);self.assertEqual(r['eligible_rom_bytes'],16)
 def test_entity_declaration_is_rejected(self):
  with self.assertRaises(ValueError):parse_dat(b'<!DOCTYPE x [<!ENTITY x "hello">]><datafile/>')
 def test_snapshot_selection_uses_date_not_larger_disc_count(self):
  with tempfile.TemporaryDirectory() as d:
   root=pathlib.Path(d)
   for name in ['Sony - Test - Datfile (1000) (2026-01-01 00-00-00).zip','Sony - Test - Datfile (999) (2026-02-01 00-00-00).zip']:
    with zipfile.ZipFile(root/name,'w') as z:z.writestr('test.dat','<datafile/>')
   r=survey(root);selected=[a for a in r['archives'] if a['latest_local_snapshot']];self.assertEqual(len(selected),1);self.assertIn('(999)',selected[0]['archive'])
 def test_aggregation_deduplicates_across_members(self):
  a=Stats();b=Stats()
  for s in (a,b):s.rom({'name':'x','size':'16','sha1':H})
  a.add(b);self.assertEqual(a.report()['repeated_file_bytes'],16)
if __name__=='__main__':unittest.main()
