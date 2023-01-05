import { useState, useEffect } from "react"


export default function CryptoCurrencies() {
    const userID = 1;
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
                `http://localhost:8000/users/${userID}/portfolio/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({title: "Test", currency_id: currency_id, amount: 1})
            })

            const res = await resp.json()
            console.log(res)
        } catch(e) {
            console.log(e)
        }
    }

    useEffect(() => {
        fetchCurrencies()
    }, [])

    return (
        <div className="lg:w-1/2 lg:absolute lg:left-1/4 md:m-10 m-5">
            <div className="m-10 text-end">
                <a href="/portfolio" className="px-5 py-2 bg-slate-300/50 rounded-lg text-sky-600 font-semibold border hover:bg-sky-200/50 hover:border-sky-300">Portfolio</a>   
            </div>
            <div className="bg-white rounded-xl">
                {currencies.map(currency => {
                    return (
                        <div className="p-2">
                            <div className="mx-5 p-3 flex justify-between">
                                <div className="flex items-center">
                                    <img src={currency.image_url} alt="logo" width="30" className="rounded-xl"/>
                                    <div className="mx-2 font-bold">{currency.name}</div>
                                </div>
                                <button 
                                    className="px-4 py-2 bg-slate-300/50 rounded-lg text-sky-600 font-semibold border hover:bg-sky-200/50 hover:border-sky-300"
                                    onClick={() => handleAddAsset(currency.id)}
                                    >Add</button>
                            </div>
                            <hr />
                        </div>
                    )
                })}
            </div>
        </div>

    )
}