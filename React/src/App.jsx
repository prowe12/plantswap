import React, { useState, useEffect } from "react"

import api from './api'
import "./index.css"
import Navbar from "./components/Navbar"
import Available from "./components/Available"
import useToken from './components/useToken'


const App = () => {

  // Set up share, which will be the recipient of the plant form data
  const [shares, setShares] = useState([]);

  // Default form data for plant shares
  const [formData, setFormData] = useState({
    amount: '',
    shared_by: '',
    description: '',
    plant_name: '',
    is_available_now: false,
    date: ''
  })

  const fetchShares = async () => {
    const response = await api.get('/shares/')
    setShares(response.data)
  };

  // What does this do?  Why
  useEffect(() => {
    fetchShares();
  }, []);

  const handleInputChange = (event) => {
    // Test condition event.target.type === 'checkbox'
    // If true, value is event.target.checked
    // If false, value is event.target.value
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    // Post, get, and set shares
    await api.post('/shares/', formData);
    fetchShares();
    // Reset the login form to blank
    setFormData({
      amount: '',
      shared_by: '',
      description: '',
      plant_name: '',
      is_available_now: false,
      date: ''
    });
  };

  const { token, setToken } = useToken()

  // Default form data for login (blank)
  const [loginFormData, setLoginFormData] = useState({
    username: '',
    full_name: '',
    password: '',
    email: '',
  })

  const handleLoginInputChange = (event) => {
    // If a value is entered in to the login form, assign
    // it to the login form data
    const value = event.target.value;
    setLoginFormData({
      ...loginFormData,
      [event.target.name]: value,
    });
  };

  const handleLoginFormSubmit = async (event) => {
    event.preventDefault();
    // Send the login form data to the token endpoint to see authenticate
    getToken(loginFormData);
    // Reset the login form to blank
    setLoginFormData({
      username: '',
      full_name: '',
      password: '',
      email: '',
    });
  };


  function getToken(content) {
    console.log(content)
    fetch("http://localhost:8000/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      // Todo: Allowed username and password hardwired here; get from form
      body: "grant_type=&username=johndoe&password=secret&scope=&client_id=&client_secret="
    }).then(function (response) {
      if (response.ok) {
        return response.json();
      }
      throw new Error('Network response was not ok.');
    }).then(function (data) {
      console.log(data);
      // Is the following an ok way to do it?
      const token = data.access_token;
      console.log("token:" + token);
      if (token) {
        console.log("that's all folks");
      };
    }).catch(function (error) {
      console.log('There has been a problem with your fetch operation: ',
        error.message);
    });
  }

  return (
    <div>
      <Navbar />

      <h2>Login</h2>
      <form onSubmit={handleLoginFormSubmit}>

        <label htmlFor='username' className='form-label'>Username</label>
        <input type='text' className='form-control' id='username' name='username' onChange={handleLoginInputChange} value={loginFormData.username} />
        <br></br>
        <label htmlFor='password' className='form-label'>Password</label>
        <input type='text' className='form-control' id='password' name='password' onChange={handleLoginInputChange} value={loginFormData.password} />
        <br></br>

        <button type='submit' className='btn btn-primary'>
          Submit
        </button>
      </form>

      {/* Send shares data to component that makes table of available plants */}
      <Available shares={shares.map((share) => (
        <tr key={(share.id)}>
          <td>{share.plant_name}</td>
          <td>{share.amount}</td>
          <td>{share.description}</td>
          <td>{share.is_available_now ? 'Yes' : 'No'} </td>
          <td>{share.shared_by}</td>
          <td>{share.date}</td>
        </tr>
      ))} />

      <div className="share_plant" id="share">
        <h1>Share a plant</h1>

        <form onSubmit={handleFormSubmit}>
          <table>
            <tbody>
              <tr>
                <td><label htmlFor='shared_by' className='form-label'>Shared by</label> </td>
                <td>
                  <input type='text' className='form-control' id='shared_by' name='shared_by' onChange={handleInputChange} value={formData.shared_by} />
                </td>
              </tr>

              <tr>
                <td><label htmlFor='plant_name' className='form-label'>Plant name</label></td>
                <td>
                  <input type='text' className='form-control' id='plant_name' name='plant_name' onChange={handleInputChange} value={formData.plant_name} />
                </td>
              </tr>

              <tr>
                <td><label htmlFor='amount' className='form-label'>
                  Amount
                </label></td>
                <td><input type='text' className='form-control' id='amount' name='amount' onChange={handleInputChange} value={formData.amount} /></td>
              </tr>

              <tr>
                <td><label htmlFor='description' className='form-label'>
                  Description
                </label></td>
                <td><input type='text' className='form-control' id='description' name='description' onChange={handleInputChange} value={formData.description} /></td>
              </tr>

              <tr>
                <td><label htmlFor='is_available_now' className='form-label'>
                  Available now?
                </label></td>
                <td> <input type='checkbox' id='is_available_now' name='is_available_now' onChange={handleInputChange} value={formData.is_available_now} />
                </td>
              </tr>

              <tr>
                <td><label htmlFor='date' className='form-label'>
                  Date
                </label></td>
                <td><input type='text' className='form-control' id='date' name='date' onChange={handleInputChange} value={formData.date} />
                </td>
              </tr>
            </tbody>
          </table>

          <button type='submit' className='btn btn-primary'>
            Submit
          </button>
        </form>

      </div >

      <div className="request_plant" id="request">
        <h1>Request a plant</h1>
      </div>

    </div >
  )
}

export default App;
