#!/usr/bin/env python3
"""Read DAT ZIPs and publish aggregate metadata only; never extract ROMs or DATs.

Python 3.10+ standard library. Exact-file estimates use declared size+SHA1;
CHD disk identities and unknown/no-dump entries are counted separately.
"""
import argparse, collections, csv, hashlib, io, json, pathlib, re, zipfile
import xml.etree.ElementTree as ET

SIDECARS={'.cue','.gdi','.sbi','.sub','.txt','.log','.mds','.ccd'}
MAX_MEMBER=256*1024**2

def family(name):
    for f in ('HBMAME','MAME','FBNeo','Demul','Visual Pinball'):
        if name.startswith(f+' '):return f
    if '(Parent-Clone)' in name or '(DB Export)' in name or '(Dump Log)' in name:return 'No-Intro'
    if any(x in name for x in (' - Datfile ',' - Cuesheets ',' - GDI Files ')):return 'Redump'
    return 'Unclassified'

def series(name):
    s=pathlib.Path(name).stem
    if family(name) in ('MAME','HBMAME','Demul'):return re.sub(r'^(MAME|HBMAME|Demul) \S+',r'\1',s)
    if family(name)=='FBNeo':return 'FBNeo ROMs (split)'
    if family(name)=='Redump':return re.sub(r' \(\d+\) \(\d{4}-\d{2}-\d{2}[^)]*\)$','',s)
    return re.sub(r' \((?:\d{8}-\d{6}|\d{4}-\d{2}-\d{2})\)$','',s)

def timestamp(name):
    dates=re.findall(r'\((\d{4}-\d{2}-\d{2}(?: \d{2}-\d{2}-\d{2})?|\d{8}-\d{6})\)',name)
    if dates:return re.sub(r'[^0-9]','',dates[-1]).ljust(14,'0')
    m=re.search(r' (\d{6}) GIT',name)
    if m:return '20'+m[1]+'000000'
    return ''

class Stats:
    def __init__(self):
        self.counts=collections.Counter();self.extensions=collections.Counter();self.statuses=collections.Counter();self.identities=set();self.media=set();self.disks=set();self.max_size=0
    def rom(self,a):
        self.counts['rom_records']+=1;self.extensions[pathlib.PurePosixPath(a.get('name','')).suffix.lower() or '(none)']+=1
        status=a.get('status','good');self.statuses[status]+=1
        if a.get('merge'):self.counts['rom_merge_attributes']+=1
        try:size=int(a['size']);assert size>=0
        except (KeyError,ValueError,AssertionError):self.counts['rom_missing_size']+=1;return
        self.counts['declared_rom_bytes']+=size;self.max_size=max(self.max_size,size)
        sha=a.get('sha1','').lower()
        if status=='nodump' or not re.fullmatch('[0-9a-f]{40}',sha):self.counts['rom_excluded_from_identity_estimate']+=1;return
        key=(size,sha);self.identities.add(key);self.counts['eligible_rom_records']+=1;self.counts['eligible_rom_bytes']+=size
        ext=pathlib.PurePosixPath(a.get('name','')).suffix.lower()
        if ext not in SIDECARS:self.media.add(key);self.counts['eligible_media_records']+=1;self.counts['eligible_media_bytes']+=size
    def disk(self,a):
        self.counts['disk_records']+=1
        sha=a.get('sha1','').lower()
        if a.get('status')!='nodump' and re.fullmatch('[0-9a-f]{40}',sha):self.disks.add(sha)
        if 'size' not in a:self.counts['disk_records_without_size']+=1
    def add(self,other):
        self.counts.update(other.counts);self.extensions.update(other.extensions);self.statuses.update(other.statuses)
        self.identities.update(other.identities);self.media.update(other.media);self.disks.update(other.disks);self.max_size=max(self.max_size,other.max_size)
    def report(self):
        r={k:self.counts[k] for k in ('sets','cloneof','romof','device_ref','rom_records','rom_merge_attributes','declared_rom_bytes','rom_missing_size','rom_excluded_from_identity_estimate','eligible_rom_records','eligible_rom_bytes','eligible_media_records','eligible_media_bytes','disk_records','disk_records_without_size')}
        r.update(unique_file_identities=len(self.identities),unique_file_bytes=sum(k[0] for k in self.identities),unique_media_identities=len(self.media),unique_media_bytes=sum(k[0] for k in self.media),unique_disk_sha1=len(self.disks),max_rom_size=self.max_size,extensions=dict(sorted(self.extensions.items())),statuses=dict(sorted(self.statuses.items())))
        r['repeated_file_bytes']=r['eligible_rom_bytes']-r['unique_file_bytes'];r['repeated_media_bytes']=r['eligible_media_bytes']-r['unique_media_bytes']
        r['repeated_file_percent']=100*r['repeated_file_bytes']/r['eligible_rom_bytes'] if r['eligible_rom_bytes'] else None
        r['repeated_media_percent']=100*r['repeated_media_bytes']/r['eligible_media_bytes'] if r['eligible_media_bytes'] else None
        return r

def parse_dat(data):
    if re.search(br'<!ENTITY\b',data,re.I):raise ValueError('Entity declarations are not accepted')
    stat=Stats();header={};root_tag=None
    for event,e in ET.iterparse(io.BytesIO(data),events=('start','end')):
        if event=='start':
            if root_tag is None:root_tag=e.tag
            continue
        if e.tag=='header':
            header={x.tag:(x.text or '').strip() for x in e if x.tag in ('name','description','version','date','author','homepage','url')};e.clear()
        elif e.tag=='rom':stat.rom(e.attrib);e.clear()
        elif e.tag=='disk':stat.disk(e.attrib);e.clear()
        elif e.tag=='device_ref':stat.counts['device_ref']+=1;e.clear()
        elif e.tag in ('game','machine','software'):
            stat.counts['sets']+=1
            for a in ('cloneof','romof'):
                if e.get(a):stat.counts[a]+=1
            e.clear()
    if root_tag not in ('datafile','mame','softwarelist'):raise ValueError('Unexpected DAT root: '+str(root_tag))
    return header,stat

def survey(root):
    files=sorted(p for p in root.rglob('*') if p.is_file());archives=[];members=[];private={}
    for p in files:
        name=str(p.relative_to(root));fam=family(name)
        if p.suffix.lower()!='.zip':raise ValueError('Unsurveyed non-ZIP file '+name)
        record={'archive':name,'family':fam,'series':series(name),'filename_timestamp':timestamp(name),'archive_bytes':p.stat().st_size,'archive_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        total=Stats()
        with zipfile.ZipFile(p) as z:
            infos=[i for i in z.infolist() if not i.is_dir()]
            record.update(member_count=len(infos),expanded_member_bytes=sum(i.file_size for i in infos),member_extensions=dict(collections.Counter(pathlib.PurePosixPath(i.filename).suffix.lower() for i in infos)))
            if '(DB Export)' in name:
                record['kind']='provenance-db-export';record['stats']=None
                # Inventory identity only: the NES importer, not a generic DAT parser,
                # handles the sibling XML roots and repeated source references.
            elif '(Dump Log)' in name:
                record['kind']='provenance-dumplog';record['stats']=None
                data=z.read(infos[0]);record['csv_data_rows']=sum(1 for _ in csv.reader(io.StringIO(data.decode('utf-8-sig')),delimiter=';'))-1
            elif ' - Cuesheets ' in name or ' - GDI Files ' in name:
                record['kind']='disc-layout-bundle';record['stats']=None
            else:
                record['kind']='dat-bundle'
                for i in infos:
                    if pathlib.PurePosixPath(i.filename).suffix.lower() not in ('.dat','.xml'):raise ValueError('Unsurveyed bundle member '+name+' / '+i.filename)
                    if i.file_size>MAX_MEMBER:raise ValueError('DAT member exceeds bound')
                    data=z.read(i);header,stats=parse_dat(data);total.add(stats)
                    members.append({'archive':name,'member':i.filename,'family':fam,'uncompressed_bytes':len(data),'member_sha256':hashlib.sha256(data).hexdigest(),'header':header,'stats':stats.report()})
                record['stats']=total.report();private[name]=total
        archives.append(record)
    latest={}
    for a in archives:
        k=a['series']
        if k not in latest or (a['filename_timestamp'],a['archive'])>(latest[k]['filename_timestamp'],latest[k]['archive']):latest[k]=a
    for a in archives:a['latest_local_snapshot']=latest[a['series']] is a
    for m in members:m['latest_local_snapshot']=next(a['latest_local_snapshot'] for a in archives if a['archive']==m['archive'])
    family_rows=[]
    for fam in sorted(set(a['family'] for a in archives)):
        selected=[a for a in archives if a['family']==fam and a['latest_local_snapshot']];s=Stats()
        for a in selected:
            if a['archive'] in private:s.add(private[a['archive']])
        family_rows.append({'aggregate_scope':'Inventory rollup across selected representation series; not an independent-collection storage baseline (especially MAME merged/split and CHD variants)','family':fam,'archive_count':sum(a['family']==fam for a in archives),'latest_series_count':len(selected),'parsed_dat_member_count':sum(m['family']==fam for m in members),'selected_dat_member_count':sum(m['family']==fam and m['latest_local_snapshot'] for m in members),'selected_aggregate':s.report()})
    chosen={}
    for a in archives:
        if not a['latest_local_snapshot'] or a['kind']!='dat-bundle':continue
        if a['family']=='FBNeo':chosen['FBNeo']=private[a['archive']]
        if a['family']=='MAME' and 'ROMs (split)' in a['archive']:chosen['MAME ROMs split']=private[a['archive']]
        if a['family']=='HBMAME' and 'Software' not in a['archive'] and ' ROMs (merged)' in a['archive']:chosen['HBMAME ROMs merged']=private[a['archive']]
        if a['family']=='Demul' and 'ROMs' in a['archive']:chosen['Demul ROMs']=private[a['archive']]
    union=set();pairwise=[]
    for key,s in chosen.items():union.update(s.identities)
    for i,(a,x) in enumerate(chosen.items()):
        for b,y in list(chosen.items())[i+1:]:
            both=x.identities&y.identities;pairwise.append({'left':a,'right':b,'shared_unique_files':len(both),'shared_unique_bytes':sum(k[0] for k in both)})
    cross={'scope':list(chosen),'sum_per_collection_unique_bytes':sum(sum(k[0] for k in s.identities) for s in chosen.values()),'union_unique_bytes':sum(k[0] for k in union),'union_unique_files':len(union),'pairwise':pairwise}
    layouts=[a for a in archives if a['family']=='MAME' and a['latest_local_snapshot'] and ' ROMs ' in a['archive']]
    layout_comparison={'archives':[a['archive'] for a in layouts],'same_declared_unique_content':len(layouts)==2 and private[layouts[0]['archive']].identities==private[layouts[1]['archive']].identities}
    cross['cross_collection_repeated_bytes']=cross['sum_per_collection_unique_bytes']-cross['union_unique_bytes']
    return {'survey_schema_version':1,'scope':'All source archives present at invocation; no original DAT/ROM/media payload exported','identity_estimator':'Declared size + SHA1 for non-nodump ROM entries; raw file occurrences only, no inherited dependency expansion; CHD disk SHA1 kept in a separate namespace','media_estimator_excludes_extensions':sorted(SIDECARS),'archive_count':len(archives),'parsed_dat_member_count':len(members),'latest_series_count':len(latest),'families':family_rows,'cross_arcade_collection':cross,'mame_rom_layout_comparison':layout_comparison,'archives':archives,'members':members}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('dat_directory',type=pathlib.Path);p.add_argument('output_directory',type=pathlib.Path);a=p.parse_args()
    report=survey(a.dat_directory);a.output_directory.mkdir(parents=True,exist_ok=True)
    (a.output_directory/'dat-survey.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    cols=['archive','family','series','kind','latest_local_snapshot','member_count','archive_bytes','archive_sha256','sets','rom_records','disk_records','eligible_rom_bytes','unique_file_bytes','repeated_file_bytes','repeated_file_percent','repeated_media_bytes','repeated_media_percent']
    with (a.output_directory/'dat-inventory.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");w.writeheader()
        for r in report['archives']:
            row={**r,**(r['stats'] or {})};w.writerow({k:row.get(k,'') for k in cols})
    print(json.dumps({'archives':report['archive_count'],'DAT_members':report['parsed_dat_member_count'],'latest_series':report['latest_series_count'],'families':[{k:r[k] for k in ('family','archive_count','parsed_dat_member_count')} for r in report['families']],'cross_arcade_collection':report['cross_arcade_collection']},indent=2))
if __name__=='__main__':main()
