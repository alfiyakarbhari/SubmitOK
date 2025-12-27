import axios from "axios"

const API = "http://localhost:8000"

export const testFirebase = () => {
  return axios.post(`${API}/test-save`)
}
