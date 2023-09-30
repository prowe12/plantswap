

import React, { useState } from 'react'
import PropTypes from 'prop-types'


async function LoginUser(credentials) {
    return fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        // Todo: Hardwired to allowed username and password; get from form
        body: "grant_type=&username=johndoe&password=secret&scope=&client_id=&client_secret="
    }).then(function (response) {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    }).then(function (data) {
        // Todo: remove the following
        console.log("token:" + data.access_token);
        return data.access_token;
    }).catch(function (error) {
        console.log('There has been a problem with your fetch operation: ',
            error.message);
    });
}



const Login = ({ setToken }) => {
    const [username, setUsername] = useState()
    const [password, setPassword] = useState()

    const handleSubmit = async (e) => {
        e.preventDefault()
        const token = await LoginUser({
            username,
            password
        })
        setToken(token)
    }
    return (
        <div>
            <h1>Sign Up Here</h1>
            <form onSubmit={handleSubmit}>
                <p>Username</p>
                <input type="text" required onChange={(e) => setPassword(e.target.value)} placeholder='johndoe' />
                <p>Password</p>
                <input type="password" required onChange={(e) => setUsername(e.target.value)} placeholder='secret' />
                <button type="submit" >Submit</button>
                <div>
                    <p><input type="checkbox" />Remember me</p>
                </div>
            </form>
            <br></br>
        </div>
    )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
}

export default Login
