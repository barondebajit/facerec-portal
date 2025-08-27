import React, { useState } from 'react'
import Camera from './components/Camera'

export default function Register(){
  const [name, setName] = useState('')
  const [capturing, setCapturing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [frames, setFrames] = useState([])
  const [result, setResult] = useState(null)

  const totalFrames = 12
  const intervalMs = 450

  async function startCapture(){
    if(!name.trim()){ alert('Enter a name first.'); return; }
    setFrames([])
    setResult(null)
    setCapturing(true)
    for(let i=0;i<totalFrames;i++){
      const blob = await window.__captureFrame()
      setFrames(prev=>[...prev, blob])
      setProgress(Math.round(((i+1)/totalFrames)*100))
      await new Promise(r=>setTimeout(r, intervalMs))
    }
    setCapturing(false)
  }

  async function submit(){
    if(!name.trim() || frames.length===0){ return }
    const fd = new FormData()
    fd.append('name', name.trim())
    frames.forEach((b, idx)=> fd.append('files', b, `frame_${idx}.jpg`))
    const res = await fetch('/api/register', { method:'POST', body: fd })
    const data = await res.json()
    setResult(data)
  }

  return (
    <div className="card">
      <h2>Register a face</h2>
      <p className="muted">Look at the camera and slowly turn your head left/right while we capture frames.</p>
      <div className="row">
        <div style={{flex:'1 1 380px'}}>
          <label>Name</label>
          <input type="text" placeholder="e.g. Alice" value={name} onChange={e=>setName(e.target.value)} />
          <div style={{display:'flex', gap:'.5rem', marginTop:'.8rem'}}>
            <button className="btn" onClick={startCapture} disabled={capturing}>🎥 Capture</button>
            <button className="btn secondary" onClick={()=>{setFrames([]); setProgress(0)}} disabled={capturing}>Reset</button>
            <button className="btn" onClick={submit} disabled={capturing || frames.length===0}>💾 Submit</button>
          </div>
          <div style={{marginTop:'.8rem'}} className="progress"><div style={{width: progress+'%'}} /></div>
          <div style={{marginTop:'.6rem'}} className="muted">{frames.length} / {totalFrames} frames</div>
          {result && <pre className="muted" style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(result, null, 2)}</pre>}
        </div>
        <div style={{flex:'1 1 380px'}}>
          <Camera />
        </div>
      </div>
    </div>
  )
}
