import { useState, useEffect } from "react"

import { getUserByEmail, fetchPortfolios } from "./Functions"


export default function CryptoCurrencies() {
    const userEmail = "example@gmail.com"
    const [userID, setUserID] = useState(0)
    const [portfolioID, setPortfolioID] = useState(0)
    const [currencies, setCurrencies] = useState([])


    const fetchCurrencies = async () => {
        try {
            const resp = await fetch("http://localhost:8000/currencies/")
            const res = await resp.json()
            setCurrencies(res)
        } catch(e) {
            console.log(e)
        }
    }

    const handleAddAsset = async (currency_id) => {
        try {
            const resp = await fetch(
                `http://localhost:8000/users/${userID}/portfolios/${portfolioID}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({title: "Test", currency_id: currency_id, amount: 1})
            })

            const res = await resp.json()
        } catch(e) {
            console.log(e)
        }
    }

    useEffect(() => {
        fetchCurrencies()
        async function getUser() {
            const id = await getUserByEmail(userEmail)
            setUserID(id)
        }

        getUser()
    }, [])

    useEffect(() => {
        if (userID === 0) return

        async function getPortfolio() {
            const id = await fetchPortfolios(userID, "Test")
            setPortfolioID(id)
        }

        getPortfolio()
    }, [userID])


    return (
        <div className="lg:w-1/2 lg:absolute lg:left-1/4 md:m-10 m-5">
            <div className="m-10 text-end">
                <a href="/portfolio" className="px-5 py-2 bg-slate-300/50 rounded-lg text-sky-600 font-semibold border hover:bg-sky-200/50 hover:border-sky-300">Portfolio</a>   
            </div>
            <div className="bg-white rounded-xl">
                {currencies.map(currency => {
                    return (
                        <div className="p-2">
                            <div className="mx-5 p-3 grid grid-cols-3 flex items-center">

                                <div className="flex items-center">
                                    <img src={currency.image_url} alt="logo" width="30" className="rounded-xl"/>
                                    <div className="mx-2 font-bold">{currency.name}</div>
                                </div>
                                <div className="">${currency.price}</div>

                                <div className="flex justify-end">
                                    <button 
                                        className="px-4 py-2 bg-slate-300/50 rounded-lg text-sky-600 font-semibold border hover:bg-sky-200/50 hover:border-sky-300"
                                        onClick={() => handleAddAsset(currency.id)}
                                        >Add
                                    </button>
                                </div>
                            </div>
                            <hr />
                        </div>
                    )
                })}
            </div>
        </div>

    )
}