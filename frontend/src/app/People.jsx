import React, { useEffect, useState } from 'react'

export default function People(){
  const [list, setList] = useState([])
  const [loading, setLoading] = useState(true)

  async function load(){
    setLoading(true)
    const res = await fetch('/api/people')
    const data = await res.json()
    setList(data.people || [])
    setLoading(false)
  }
  useEffect(()=>{ load() }, [])

  async function del(name){
    if(!confirm(`Delete ${name}?`)) return
    await fetch('/api/people/'+encodeURIComponent(name), { method:'DELETE' })
    load()
  }

  return (
    <div className="card">
      <h2>Registered people</h2>
      {loading ? <div className="muted">Loading…</div> : (
        list.length === 0 ? <div className="muted">No one registered yet.</div> : (
          <table>
            <thead><tr><th>Name</th><th></th></tr></thead>
            <tbody>
              {list.map(n => (
                <tr key={n}>
                  <td>{n}</td>
                  <td style={{textAlign:'right'}}><button className="btn secondary" onClick={()=>del(n)}>Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        )
      )}
    </div>
  )
}
