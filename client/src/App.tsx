import { useState, useEffect } from 'react'
import { io } from 'socket.io-client';

type Messages = {
  W: string | undefined,
  Muna: string | undefined
}

function App() {
  const [message, setMessage] = useState<Messages>(); // 0 = W, 1 = Muna
  
  useEffect(() => {
      const socket = io("http://127.0.0.1:5000");

      socket.on("connect", () => {
        console.log("connected; turning on chat");
        socket.emit("server_loop");
      });

      socket.on("disconnect", () => {
        console.log("disconnected");

        setMessage({W: "(Disconnected)", Muna: "(Disconnected)"})
      });

      socket.on("chat_response", (data) => {
        data = JSON.parse(data);

        if (data.Muna === "") {
          data.Muna = "(Awaiting input...)";
        }

        if (data.W === "") {
          data.W = "(Responding...)";
        }

        console.log("Message (to_array): " + data);

        setMessage(data);
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
      
      <div className='grid grid-cols-3 '>

        <div>

          <div className='py-5'>

            <h3>Muna says:</h3>

          </div>

          <div className='bg-red-950 w-1/2 mx-auto p-5 rounded-md'>
            {
              // THIS SHIT TOOK ME A FUCKING HOUR TO FIGURE OUT
              // ENSURE YOU PUT A CONDITION SO THAT IT CALLS THE API
              message === undefined ? <p>(Hasn't Said Anything Yet...)</p> : 
              message.Muna
            }
          </div>

        </div>

        <div>

          <img src='https://preview.redd.it/favorite-w-face-v0-2gany80afosb1.png?width=640&crop=smart&auto=webp&s=692782bebe88d23ba6d4b20fbe307ef2da863a66' className='w-1/2 mx-auto' />
        
          <div className='bg-slate-800 w-60 h-96 mx-auto p-5 m-5' >

            <div className='bg-orange-800 p-5'>

              <h1>Pause</h1>

            </div>

          </div>   

        </div>

        <div>
          <div className='py-5'>

            <h3>W says:</h3>
            
          </div>
          <div className='bg-red-950 w-1/2 mx-auto p-5 rounded-md'>
            {
              message === undefined ? <p>(Hasn't Said Anything Yet...)</p> : 
              message.W
            }
          </div>


        </div>
      </div>


    </div>
  );
}

export default App;