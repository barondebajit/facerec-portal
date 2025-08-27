import React, { useEffect, useRef, useState } from 'react'

export default function Camera({width=640, height=480}){
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const [ready, setReady] = useState(false)
  const [stream, setStream] = useState(null)

  useEffect(()=>{
    let mounted = true
    async function start(){
      try{
        const s = await navigator.mediaDevices.getUserMedia({video: { width, height }})
        if(!mounted) return
        setStream(s)
        if(videoRef.current){
          videoRef.current.srcObject = s
          await videoRef.current.play()
          setReady(true)
        }
      }catch(err){
        console.error(err)
        alert("Unable to access camera. Please allow permissions.")
      }
    }
    start()
    return ()=>{
      mounted = false
      if(stream){
        stream.getTracks().forEach(t=>t.stop())
      }
    }
  }, [])

  const captureBlob = () => {
    const video = videoRef.current
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    return new Promise(resolve => canvas.toBlob(b=>resolve(b), 'image/jpeg', 0.9))
  }

  return (
    <div className="video-box">
      <video ref={videoRef} playsInline muted />
      <canvas ref={canvasRef} style={{display:'none'}} />
      <div style={{position:'absolute', top:8, left:8}} className="pill">{ready? 'Camera ready' : 'Starting camera...'}</div>
      <CaptureHandle getter={captureBlob} />
    </div>
  )
}

function CaptureHandle({getter}){
  React.useEffect(()=>{
    window.__captureFrame = getter
    return ()=>{ delete window.__captureFrame }
  }, [getter])
  return null
}
