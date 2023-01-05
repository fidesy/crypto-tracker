import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import CryptoCurrencies from "./CryptoCurrencies"

import Dashboard from "./Dashboard"


export default function App() {
    return (
        <Router>

            <Routes>
                <Route path="/" element={<CryptoCurrencies />}/>
                <Route path="/portfolio" element={<Dashboard />}/>
            </Routes>

        </Router>
    )
}