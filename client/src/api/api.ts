import axios from "axios";

export const get_convo = async (setArray: any) => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/api/convo");
    const response: any = [res.data.W, res.data.Muna];
    setArray(response);
  } catch (error) {
    console.error(error);
  }
}

export const set_pause = async (paused: boolean) => {
    const res = await axios.post("/api/pause");
    console.log(res.data.Paused);
  }