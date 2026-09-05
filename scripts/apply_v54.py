from pathlib import Path

index = Path('public/index.html')
s = index.read_text()
s = s.replace('<link rel="stylesheet" href="/mobile-v52.css?v=53" />', '<link rel="stylesheet" href="/theme-v54.css?v=54" />\n  <link rel="stylesheet" href="/mobile-v54.css?v=54" />')
if 'id="themeBtn"' not in s:
    s = s.replace('<button class="icon-btn" id="refreshBtn">↻</button>', '<button class="icon-btn" id="themeBtn" type="button" aria-label="Toggle theme" title="Toggle theme">☀</button><button class="icon-btn" id="refreshBtn">↻</button>')
if '<script src="theme.js?v=54"></script>' not in s:
    s = s.replace('<script src="app.js"></script>', '<script src="theme.js?v=54"></script>\n  <script src="app.js?v=54"></script>')
index.write_text(s)

server = Path('server.js')
s = server.read_text()
old = "app.get('/api/market-data',async(req,res)=>res.json({updated_at:new Date().toISOString(),source:'safe-mode',transfers:[],images:[],warning:'Transfer enrichment temporarily disabled to protect the Render Free memory limit.'}));"
new = '''function parseCsvLine(line){const out=[];let cell='',q=false;for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'){if(q&&line[i+1]==='"'){cell+='"';i++}else q=!q}else if(c===','&&!q){out.push(cell);cell=''}else cell+=c}out.push(cell);return out}
async function loadRecentPlTransfers(teams,ttl=21600000){
  const key='market:pl-transfers',hit=cache.get(key);if(hit&&Date.now()-hit.ts<ttl)return hit.data;
  const r=await fetch(`${MARKET_BASE}/transfers.csv.gz`,{headers:{'User-Agent':'Hisho-FPL-Hub/5.4'}});if(!r.ok||!r.body)throw new Error(`Transfer dataset ${r.status}`);
  const {Readable}=await import('node:stream'),{createInterface}=await import('node:readline');
  const input=Readable.fromWeb(r.body).pipe(zlib.createGunzip()),rl=createInterface({input,crlfDelay:Infinity});
  let headers=null;const rows=[];
  for await(const line of rl){if(!line)continue;const cells=parseCsvLine(line);if(!headers){headers=cells;continue}const row=Object.fromEntries(headers.map((h,i)=>[h,cells[i]??'']));const d=String(row.transfer_date||'');if(d<'2025-06-01')continue;if(!isCurrentPlClub(row.from_club_name,teams)&&!isCurrentPlClub(row.to_club_name,teams))continue;rows.push(row)}
  rows.sort((a,b)=>String(b.transfer_date).localeCompare(String(a.transfer_date)));const data=rows.slice(0,1000);cache.set(key,{ts:Date.now(),data});return data
}
app.get('/api/market-data',async(req,res)=>{try{const bootstrap=await cachedJson(`${FPL}/bootstrap-static/`,300000),transfers=await loadRecentPlTransfers(bootstrap.teams||[]);res.json({updated_at:new Date().toISOString(),source:'dcaribou/transfermarkt-datasets (streamed, weekly refresh)',transfers,images:[]})}catch(e){res.status(502).json({error:e.message,transfers:[],images:[]})}});'''
if old in s:
    s = s.replace(old, new)
elif "source:'safe-mode'" in s:
    raise RuntimeError('safe-mode endpoint changed unexpectedly')
server.write_text(s)
