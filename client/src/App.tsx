import { useState, useEffect } from 'react'
import { get_convo } from './api/api';

function App() {
  const [arrr, setArray] = useState([]); // 0 = W, 1 = Muna
  
  useEffect(() => {
    const interval = setInterval(get_convo, 5000, setArray);
    return () => clearInterval(interval);
  }, [])
 
  return (
    <div className='h-lvh bg-neutral-900 p-5'>

      <h1 className='text-4xl'>W, the AI Shithead</h1>

      <br />
      
      <div className='py-5'>
        <h3>W says:</h3>
      </div>
      <div className='bg-red-950 w-1/2 mx-auto p-5 rounded-md'>
        {
          // THIS SHIT TOOK ME A FUCKING HOUR TO FIGURE OUT
          // ENSURE YOU PUT A CONDITION SO THAT IT CALLS THE API
          arrr.length <= 0 ? <p>(Hasn't Said Anything Yet...)</p> : 
          arrr[0]
        }
      </div>

      <div className='bg-W w-[50%] h-96 mx-auto bg-cover bg-center my-5'></div>

      <div className='py-5'>
        <h3>Muna says:</h3>
      </div>
      <div className='bg-red-950 w-1/2 mx-auto p-5 rounded-md'>
        {
          arrr.length <= 0 ? <p>(Hasn't Said Anything Yet...)</p> : 
          arrr[1]
        }
      </div>

      <div className='bg-slate-800 w-60 h-96 mx-auto p-5 m-5' >
        <div className='bg-orange-800 p-5'>
          <h1>Pause</h1>
        </div>
      </div>
    </div>
  );
}

export default App;