import React, { useState, useEffect } from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"

import api from "./../api"
import Available from "./Available"
import Login from './Login'


const Dashboard = () => {
    const [token, setToken] = useState()
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

    // What does this do?
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
        console.log(token)
        if (token) {
            await api.post('/shares/', formData);
            fetchShares();
        }
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

    if (!token) {
        // If the user has not logged in, show only the available plants
        {
            return (
                <div>
                    <div>
                        <Login setToken={setToken} />
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
                    </div>

                    <div className="share_plant" id="share">
                        <h1>Share Plants</h1>
                        <p>Please log in to add plants to share.</p>
                    </div>
                    <div className="request_plant" id="request">
                        <h1>Request Plants</h1>
                        <p>Please log in to request plants.</p>
                    </div>
                </div>
            )
        }
    }
    return (
        // If the user *has* logged in, also show forms to add/delete plants
        <div>

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

export default Dashboard
