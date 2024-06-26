import React, { useState } from 'react'
import useForm,{ FormProvide } from '../context/useForm'
import Form from './Form'
import Graph from './Graph'
import '../css/MiddleLayer.css'

function MiddleLayer() {
    const [user,setUser]=useState("")
  return (
    <FormProvide value={{user,setUser}}>
    <div className='container'>
<div className="form">
<Form/>
</div>
<div className="graph">
    <Graph/>
</div>
    </div>
    </FormProvide>
  )
}

export default MiddleLayer