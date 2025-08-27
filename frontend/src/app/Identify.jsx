import React, { useState } from 'react'
import Camera from './components/Camera'

export default function Identify(){
  const [result, setResult] = useState(null)
  const [busy, setBusy] = useState(false)

  async function identifyOnce(){
    setBusy(true); setResult(null)
    const blob = await window.__captureFrame()
    const fd = new FormData()
    fd.append('files', blob, 'frame.jpg')
    const res = await fetch('/api/identify', { method:'POST', body: fd })
    const data = await res.json()
    setResult(data)
    setBusy(false)
  }

  return (
    <div className="card">
      <h2>Identify a face</h2>
      <p className="muted">Click Identify to snap a frame and match it against registered faces.</p>
      <div className="row">
        <div style={{flex:'1 1 380px'}}>
          <button className="btn" onClick={identifyOnce} disabled={busy}>🔎 Identify</button>
          {result && (
            <div style={{marginTop:'.8rem'}}>
              <h3>Result</h3>
              <div className="candidates">
                <div><strong>{result.unknown ? 'Unknown' : result.name}</strong> <span className="pill">score {result.score?.toFixed ? result.score.toFixed(3) : result.score}</span></div>
                <div className="muted">Top candidates:</div>
                {result.candidates?.map((c, idx)=> (
                  <div key={idx} className="muted">#{idx+1} {c.name} — {c.score?.toFixed ? c.score.toFixed(3) : c.score}</div>
                ))}
              </div>
            </div>
          )}
        </div>
        <div style={{flex:'1 1 380px'}}>
          <Camera />
        </div>
      </div>
    </div>
  )
}
