import { useEffect, useState } from "react";
import Chart from "./Chart";


export default function Dashboard() {
    const userID = 1
    const [portfolio, setPortfolio] = useState([]) 
    const [candlesticks, setCandlesticks] = useState([])
    const [symbol, setSymbol] = useState("btcusdt")


    const fetchPortfolio = async () => {
        try {
            const resp = await fetch(`http://localhost:8000/users/${userID}/portfolio/`)
            const res = await resp.json()
            setPortfolio(res)
        } catch(e) {
            console.log(e)
        }
    }

    const fetchCandlesticks = async () => {
        try {
            const resp = await fetch(`http://localhost:8000/klines/${symbol}/`)
            const res = await resp.json()
            setCandlesticks(res)
        } catch(e) {
            console.log(e)
        }
    }


    const handleChangeAmount = async (portfolio_id, value) => {
        if (value.length == 0 || value.length == 1 && value == "0" || value.length == 2 && value == "0.") {
            let portfolio_ = portfolio.map(asset => {
                if (asset.id === portfolio_id) {
                    asset.amount = value
                }
                return asset
            })
            setPortfolio(portfolio_)
            return
        }

        let amount = parseFloat(value)
        console.log(value, amount)
        if (isNaN(amount)) {
            return
        }

        try {
            const resp = await fetch(
                `http://localhost:8000/users/${userID}/portfolio/`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({id: portfolio_id, amount: amount})
            })

            if (resp.status === 200) {
                let portfolio_ = portfolio.map(asset => {
                    if (asset.id === portfolio_id) {
                        asset.amount = amount
                    }
                    return asset
                })
                setPortfolio(portfolio_)
            }
        } catch(e) {
            console.log(e)
        }
    }

    const handleDelete = async (portfolio_id) => {
        try {
            const resp = await fetch(
                `http://localhost:8000/users/${userID}/portfolio/${portfolio_id}/`, { method: "DELETE" })

            if (resp.status == 200) {
                let portfolio_ = portfolio.filter(p => p.id != portfolio_id)
                setPortfolio(portfolio_)
            }
        } catch(e) {
            console.log(e)
        }
    }

    useEffect(() => {
        fetchPortfolio()
    }, [])

    useEffect(() => {
        fetchCandlesticks()
    }, [symbol])
               
    return (
       <div id="dashboard" className="xl:w-1/2 xl:absolute xl:left-1/4 md:m-10 m-5">
            <div className="m-10 text-end">
                <a href="/" className="px-5 py-2 bg-slate-300/50 rounded-lg text-sky-600 font-semibold border hover:bg-sky-200/50 hover:border-sky-300">Currencies</a>   
            </div>

            <div className="p-5 bg-white rounded-lg">
                <Chart candlesticks={candlesticks} title={symbol.toUpperCase()}/>
            </div>


            <div id="portfolio" className="mt-10">
                {portfolio.length == 0 && <h2 className="text-center text-2xl">You currently do not have any asset in portfolio.</h2>}
                <div className="bg-white rounded-lg">
                    {portfolio.length != 0 && portfolio.map(asset => {
                        return (
                            <div className={"flex justify-between items-center " + (symbol === asset.currency.symbol ? "bg-slate-200/50" : "")} onClick={() => setSymbol(asset.currency.symbol)}>
                                <div className="mx-5 p-5 flex items-center">
                                    <img src={asset.currency.image_url} alt="logo" width="40" className="rounded-xl"/>
                                    <div className="mx-5 font-bold">{asset.currency.name}</div>
                                </div>
                                <input type="text" className="rounded-lg p-2 bg-transparent outline-0" value={asset.amount} onChange={({target}) => handleChangeAmount(asset.id, target.value)}/>
                                <button 
                                    className="mx-4 px-5 p-2 bg-red-500/50 rounded-xl font-bold hover:bg-red-500"
                                    onClick={() => handleDelete(asset.id)}
                                    >
                                        Delete
                                </button>
                            </div>
                        )
                    })}
                </div>
            </div>
       </div>
    )
}