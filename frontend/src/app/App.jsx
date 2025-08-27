import React, { useState } from 'react'
import Register from './Register'
import Identify from './Identify'
import People from './People'

export default function App(){
  const [tab, setTab] = useState('identify')
  return (
    <>
      <header>
        <h1>👤 FaceRec Portal</h1>
        <nav>
          <a href="#" className={tab==='identify'?'active':''} onClick={()=>setTab('identify')}>Identify</a>
          <a href="#" className={tab==='register'?'active':''} onClick={()=>setTab('register')}>Register</a>
          <a href="#" className={tab==='people'?'active':''} onClick={()=>setTab('people')}>People</a>
        </nav>
      </header>
      <main>
        {tab==='identify' && <Identify />}
        {tab==='register' && <Register />}
        {tab==='people' && <People />}
      </main>
      <footer><small>Local demo • Camera data stays in your browser until you click submit.</small></footer>
    </>
  )
}
