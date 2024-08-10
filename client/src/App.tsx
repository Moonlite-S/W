import { useState, useEffect } from 'react'
import { io } from 'socket.io-client';

function App() {
  const [arrr, setArray] = useState<string[]>([]); // 0 = W, 1 = Muna
  
  useEffect(() => {
      const socket = io("http://127.0.0.1:5000");

      socket.on("connect", () => {
        console.log("connected; turning on chat");
        socket.emit("server_loop");
      });

      socket.on("disconnect", () => {
        console.log("disconnected");
      });

      socket.on("chat_response", (data) => {
        data = JSON.parse(data);
        const to_array = [data.W, data.Muna];
        console.log("Message (to_array): " + to_array);

        setArray(to_array);
      });

      socket.on("error", (data) => {
        console.log(data);
      });

      socket.on("reconnect", (attempt) => {
        console.log(attempt);
      });

      return function cleanup() {
        socket.disconnect();
      };
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