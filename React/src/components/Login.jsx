

import React, { useState } from 'react'
import PropTypes from 'prop-types'


async function LoginUser(credentials) {
    return fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        // Send username and password
        body: "grant_type=&username=" + credentials.username + "&password=" + credentials.password + "&scope=&client_id=&client_secret="
    }).then(function (response) {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    }).then(function (data) {
        return data.access_token;
    }).catch(function (error) {
        // console.log('There was a problem with your fetch operation: ',
        //     error.message);
        return 
    });
}



const Login = ({ setToken, setUsername}) => {
    const [loginMsg, setLoginMsg] = useState("")
    const [username, setUsernameHere] = useState()
    const [password, setPassword] = useState()

    const handleSubmit = async (e) => {
        e.preventDefault()
        const token = await LoginUser({
            username,
            password
        })
        setToken(token)
        if (token) {
            setUsername(username)
            setLoginMsg(username)
        }
        else setLoginMsg("Incorrect username or password, please retry.");
    }
    return (
        <div>
            <h1>Sign in</h1>
            <form onSubmit={handleSubmit}>
                <p>Username</p>
                <input type="text" required onChange={(e) => setUsernameHere(e.target.value)} placeholder='johndoe' />
                <p>Password</p>
                <input type="password" required onChange={(e) => setPassword(e.target.value)} placeholder='secret' />
                <button type="submit" >Submit</button>
                {/* <div>
                    <p><input type="checkbox" />Remember me</p>
                </div> */}
            </form>

            <br></br>
            <br></br>
            <p>{loginMsg}</p>
        </div>
    )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
}

export default Login
