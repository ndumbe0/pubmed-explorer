import { useState } from 'react';
export default function Search(){
  const [q,setQ]=useState(''); const [res,setRes]=useState<any[]>([]);
  const search=async()=>{const r=await fetch(`/api/pubmed/search?q=${encodeURIComponent(q)}&limit=50`);setRes(await r.json())};
  return <div className="p-4"><h1 className="text-2xl font-bold mb-4">Search</h1><input value={q} onChange={e=>setQ(e.target.value)} className="border p-2"/><button onClick={search} className="ml-2 bg-blue-500 text-white p-2">Search</button><div className="mt-4">{res.map((x,i)=>(<div key={i} className="border p-2 mb-2"><div className="font-bold" dangerouslySetInnerHTML={{__html:x.title}}></div><div dangerouslySetInnerHTML={{__html:x.snippet}}></div></div>))}</div></div>
}
