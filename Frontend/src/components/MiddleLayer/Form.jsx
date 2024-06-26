import React, { useEffect, useState } from 'react'
import '../css/Form.css'
import useForm from '../context/useForm'
import axios from 'axios';

function Form() {
 
  const {setUser,user}=useForm()
  const [symbol,setSymbol]=useState("")
  const [fromdate,setFromdate]=useState("")
  const [todate,setTodate]=useState("")

  console.log(user)
  function formatDate(date) {
    date=new Date(date)
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear().toString().slice(-4); // Get last two digits of the year
        return `${day}-${month}-${year}`;
  }
  const addUser=(e)=>{
e.preventDefault()
if (!symbol.length || !fromdate.length || !todate.length){
  alert("fill all field")
  return 
}
let from_date= formatDate(fromdate)
let to_date=formatDate(todate)
console.log(symbol,from_date,to_date)

axios
            .post('/api/fetch-data', { symbol, from_date, to_date })
            .then((response) => {
              console.log(response.data,"data")
                setUser(response.data);
            })
            .catch((error) => console.error(error));
setSymbol("")
setFromdate("")
setTodate("")
  }
  return (
   <>
   <div className="formcontainer">
<h1>Enter The Deatils:</h1>
    <form action="" className='formbox' id='submit'>
      <div className='inputStyle'>
        <label htmlFor="">Symbol:</label>
      <input type="text" placeholder='Enter the symbol' 
      value={symbol}
      onChange={(e)=>setSymbol((e.target.value).toUpperCase())}
      name='symbol' />

      </div>
      <div className='inputStyle'>
        <label htmlFor="">From-Date:</label>
      <input type="date" placeholder='Enter From-Date'
      
        value={fromdate}
      onChange={(e)=>setFromdate(e.target.value)}
       className='from_date' name='from-date'/>

      </div>
      <div className='inputStyle'>
        <label htmlFor="">To-Date:</label>
      <input type="date" placeholder='Enter To-date' 
        value={todate}
      onChange={(e)=>setTodate(e.target.value)}
      className='to-date'/>

      </div>
        <div className='Button'>
        
      <button type='submit' onClick={addUser}>Submit</button>

      </div>
    </form>
   </div>
   </>
  )
}

export default Form