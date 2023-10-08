

import React, { useState } from 'react'
import PropTypes from 'prop-types'


// @app.post("/users/", response_model=schemas.User)
// def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
//     db_user = crud.get_user_by_email(db, email=user.email)
//     if db_user:
//         raise HTTPException(status_code=400, detail="Email already registered")
//     return crud.create_user(db=db, user=user)



async function RegisterUser(credentials) {
    return fetch("http://localhost:8000/users/", {
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
        // Todo: remove the following
        return "Welcome " + data.username + "!  You have successfully registered. Please sign in.";
    }).catch(function (error) {
        // console.log('There was a problem with your fetch operation: ',
        //     error.message);
        return "Username " + credentials.username + " already in use, try a different one.";
    });
}



const Register = () => {
    const [username, setUsername] = useState()
    const [welcomeMsg, setWelcomeMsg] = useState("")
    const [password, setPassword] = useState()

    const handleSubmit = async (e) => {
        e.preventDefault()
        const welcome_msg = await RegisterUser({
            username, password
        })
        setWelcomeMsg(welcome_msg)
    }
    return (
        <div>
            <h1>Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <p>Email</p>
                <input type="text" required onChange={(e) => setUsername(e.target.value)} placeholder='john@doe.com' />
                <p>Password</p>
                <input type="password" required onChange={(e) => setPassword(e.target.value)} placeholder='secret' />
                <button type="submit" >Submit</button>

                <br></br>
                <br></br>
                <p>{welcomeMsg}</p>
                
            </form>
            <br></br>
        </div>
    )
}


export default Register
