import React, { useState, useEffect } from "react"

import api from './api'
import "./index.css"
import Navbar from "./components/Navbar"
import Dashboard from './components/Dashboard'

const App = () => {
  return (
    <div>
      <Navbar />


      <Dashboard />
    </div >
  )
}

export default App;
