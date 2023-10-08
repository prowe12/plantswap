import React, { useState, useEffect } from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"

import api from "./../api"
import Available from "./Available"
import Requested from "./Requested"
import Login from "./Login"
import Register from "./Register"
import FilterButton from "./FilterButton"

const FILTER_MAP = {
    "All": (share, username) => true,
    "My shares": (share, username) => (share.shared_by === username),
    "Shared by others": (share, username) => (share.shared_by !== username),
};
const FILTER_NAMES = Object.keys(FILTER_MAP);


const REQUEST_FILTER_MAP = {
    "All": (request, username) => true,
    "My requests": (request, username) => (request.requested_by === username),
    "Requested by others": (share, username) => (request.requested_by !== username),
};

const REQUEST_FILTER_NAMES = Object.keys(REQUEST_FILTER_MAP);


const Dashboard = () => {

    const [filter, setFilter] = useState("All");
    const filterList = FILTER_NAMES.map((name) => (
        <FilterButton
        key={name}
        name={name}
        isPressed={name === filter}
        setFilter={setFilter} />
      ));

    const [username, setUsername] = useState()
    const [token, setToken] = useState()

    // PLANT SHARES
    // Set up shares, which will be the recipient of the plant form data
    const [shares, setShares] = useState([]);

    // Set up shares that will be displayed on the table, which may be a
    // subset of all shares (such as only the user's shared plants)
    const filterFun = (share) => (FILTER_MAP[filter](share, username));
    const shareList = shares.filter(filterFun);
    // const shareList = filter === "All" ? shares : shares.filter(share => share.shared_by === username)
      

    // Default form data for plant shares
    const [formData, setFormData] = useState({
        shared_by: '',
        plant_name: '',
        amount: '',
        description: '',
        is_available_now: false,
        date: ''
    })

    // Assign to shares the data from the shares endpoint
    const fetchShares = async () => {
        const response = await api.get('/shares/')
        setShares(response.data)
    };

    // PLANT REQUESTS
    // Set up request, which will be the recipient of the plant form data
    const [requests, setRequests] = useState([]);

    // Default form data for plant requests
    const [requestFormData, setRequestFormData] = useState({
        requested_by: '',
        plant_name: '',
        amount: '',
        notes: '',
        date: ''
    })

    const fetchRequests = async () => {
        const response = await api.get('/requests/')
        setRequests(response.data)
    };

    // Get shares and requests data from their endpoints at mount (first render)
    // to fill out the Available and Requested plants tables
    useEffect(() => {
        fetchShares();
        fetchRequests();
    }, []);


    // Add user inputs to plant share form
    const handleInputChange = (event) => {
        // Test condition event.target.type === 'checkbox'
        // If true, value is event.target.checked
        // If false, value is event.target.value
        const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
        const datevalue = new Date().toLocaleDateString();

        setFormData({
            ...formData,
            [event.target.name]: value,
            date: datevalue,
            shared_by: username,
        });
    };

    // Post plant share form to endpoint when the user submits it 
    // (so it can be added to the database), and add it to the shares table.
    // Then reset the share form fields to blank
    const handleFormSubmit = async (event) => {
        event.preventDefault();
        // Post, get, and set shares
        console.log(token)
        if (token) {
            await api.post('/shares/', formData);
            fetchShares();
        }
        // Reset the shares form to blank
        setFormData({
            amount: '',
            description: '',
            plant_name: '',
            is_available_now: false,
        });
    };


    // Add user inputs to plant request form
    const handleRequestInputChange = (event) => {
        const value = event.target.value;
        const datevalue = new Date().toLocaleDateString();

        setRequestFormData({
            ...requestFormData,
            [event.target.name]: value,
            date: datevalue,
            requested_by: username,
        });
    };


    // Post plant request form to endpoint when the user submits it 
    // (so it can be added to the database), and add it to the requests table.
    // Then reset the request form fields to blank
    const handleRequestFormSubmit = async (event) => {
        event.preventDefault();
        // Post, get, and set requests
        if (token) {
            await api.post('/requests/', requestFormData);
            fetchRequests();
        }
        // Reset the requests form to blank
        setRequestFormData({
            requested_by: '',
            amount: '',
            notes: '',
            plant_name: '',
            date: ''
        });
    };


    if (!token) {
        // If the user has not logged in, do not show submit forms
        // instead show sign up and login
        {
            return (
                <div>
                    {/* Registration form */}
                    <div>
                        <Register setToken={setToken} setUsername={setUsername} />
                    </div>

                   {/* Login form */}
                    <div>
                        <Login setToken={setToken} setUsername={setUsername} />
                    </div>

                    {/* Table of available plants */}
                    <div>
                        {/* Send shares data to component that makes table of available plants */}
                        <Available shares={shares} />
                    </div>

                    {/* Table of requested plants */}
                    <div>
                        {/* Send request data to component that makes table of requested plants */}
                        <Requested requests={requests} />
                    </div>

                    {/* Display a note that the user must log in to share plants */}
                    <div className="share_plant" id="share">
                        <h1>Share Plants</h1>
                        <p>Please log in to add plants to share.</p>
                    </div>

                    {/* Display a note that the user must log in to request plants */}
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
            {/* Filter for available/shared plants */}
            <div className="filters btn-group stack-exception">
                {filterList}
            </div>

            {/* Table of available/shared plants */}
            <div>
                {/* Send shares data to component that makes table of available plants */}
                <Available shares={shareList} />
            </div>

            {/* Table of requested plants */}
            <div>
                {/* Send request data to component that makes table of requested plants */}
                <Requested requests={requests} />
            </div>


            {/* Form for sharing a plant */}
            <div className="share_plant" id="share">
                <h1>Share a plant</h1>
                <form onSubmit={handleFormSubmit}>
                    <table>
                        <tbody>

                            <tr>
                                <td><label htmlFor='plant_name' className='form-label'>Plant name</label></td>
                                <td>
                                    <input
                                    type='text'
                                    className='form-control'
                                    id='plant_name'
                                    name='plant_name'
                                    onChange={handleInputChange}
                                    value={formData.plant_name} />
                                </td>
                            </tr>

                            <tr>
                                <td><label htmlFor='amount' className='form-label'>Amount</label></td>
                                <td><input type='text' className='form-control' id='amount' name='amount' onChange={handleInputChange} value={formData.amount} /></td>
                            </tr>

                            <tr>
                                <td><label htmlFor='description' className='form-label'>Description</label></td>
                                <td><input type='text' className='form-control' id='description' name='description' onChange={handleInputChange} value={formData.description} /></td>
                            </tr>

                            <tr>
                                <td><label htmlFor='is_available_now' className='form-label'>
                                    Available now?
                                </label></td>
                                <td> <input
                                type='checkbox'
                                id='is_available_now'
                                name='is_available_now'
                                onChange={handleInputChange}
                                checked={formData.is_available_now} />
                                </td>
                            </tr>

                        </tbody>
                    </table>

                    <button type='submit' className='btn btn-primary'>
                        Submit
                    </button>
                </form>

            </div >

            {/* Form for requesting a plant */}
            <div className="request_plant" id="request">
                <h1>Request a plant</h1>
                <form onSubmit={handleRequestFormSubmit}>
                    <table>
                        <tbody>

                            <tr>
                                <td><label htmlFor='req_plant_name' className='form-label'>Plant name</label></td>
                                <td>
                                    <input type='text' className='form-control' id='req_plant_name' name='plant_name' onChange={handleRequestInputChange} value={requestFormData.plant_name} />
                                </td>
                            </tr>

                            <tr>
                                <td><label htmlFor='req_amount' className='form-label'>
                                    Amount
                                </label></td>
                                <td><input type='text' className='form-control' id='req_amount' name='amount' onChange={handleRequestInputChange} value={requestFormData.amount} /></td>
                            </tr>

                            <tr>
                                <td><label htmlFor='req_notes' className='form-label'>
                                    Notes
                                </label></td>
                                <td><input type='text' className='form-control' id='req_notes' name='notes' onChange={handleRequestInputChange} value={requestFormData.notes} /></td>
                            </tr>

                            {/* <tr>
                                <td><label htmlFor='requested_by' className='form-label'>
                                    Requested by
                                </label></td>
                                <td><input type='text' className='form-control' id='requested_by' name='requested_by' onChange={handleRequestInputChange} value={requestFormData.requested_by} /></td>
                            </tr> */}

                        </tbody>
                    </table>

                    <button type='submit' className='btn btn-primary'>
                        Submit
                    </button>
                </form>
            </div>


        </div >
    )
}

export default Dashboard
