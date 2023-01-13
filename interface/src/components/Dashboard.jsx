import { useEffect, useState } from "react";
import Chart from "./Chart";


export default function Dashboard() {
    const userID = 1
    const [portfolioID, setPortfolioID] = useState(1)
    const [portfolio, setPortfolio] = useState([]) 
    const [candlesticks, setCandlesticks] = useState([])
    // const [symbol, setSymbol] = useState("btcusdt")

    const createPortfolio = async () => {
        try {
            const resp = await fetch(
                `http://localhost:8000/users/${userID}/portfolios/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({title: "Test"})
            })
            const res = await resp.json()
            if (res.id === 1) {
                setPortfolioID(res.id)
            }

        } catch(e) {
            console.log(e)
        }
    }

    const fetchPortfolio = async () => {
        try {
            const resp = await fetch(`http://localhost:8000/users/${userID}/portfolios/${portfolioID}/`)
            const res = await resp.json()
            console.log(res)
            setPortfolio(res.assets)
        } catch(e) {
            console.log(e)
        }
    }

    // const fetchCandlesticks = async () => {
    //     try {
    //         const resp = await fetch(`http://localhost:8000/klines/${symbol}/`)
    //         const res = await resp.json()
    //         setCandlesticks(res)
    //     } catch(e) {
    //         console.log(e)
    //     }
    // }

    const fetchPortfolioPrices = async () => {
        try {
            const resp = await fetch(`http://localhost:8000/users/${userID}/portfolios/${portfolioID}/prices`)
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
        if (isNaN(amount)) {
            return
        }

        try {
            const resp = await fetch(
                `http://localhost:8000/users/${userID}/portfolios/${portfolioID}/`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({id: portfolio_id, amount: amount, currency_id: 0})
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
                `http://localhost:8000/users/${userID}/portfolios/1/assets/${portfolio_id}/`, { method: "DELETE" })

            if (resp.status == 200) {
                let portfolio_ = portfolio.filter(p => p.id != portfolio_id)
                setPortfolio(portfolio_)
            }
        } catch(e) {
            console.log(e)
        }
    }

    useEffect(() => {
        createPortfolio()
    }, [portfolioID])

    useEffect(() => {
        fetchPortfolio()
    }, [])

    useEffect(() => {
        // fetchCandlesticks()
        fetchPortfolioPrices()
    }, [portfolio])
               
    return (
       <div id="dashboard" className="xl:w-1/2 xl:absolute xl:left-1/4 md:m-10 m-5">
            <div className="m-10 text-end">
                <a href="/" className="px-5 py-2 bg-slate-300/50 rounded-lg text-sky-600 font-semibold border hover:bg-sky-200/50 hover:border-sky-300">Currencies</a>   
            </div>

            <div className="p-5 bg-white rounded-lg">
                <Chart candlesticks={candlesticks} title="Portfolio"/>
            </div>


            <div id="portfolio" className="mt-10">
                {portfolio.length == 0 && <h2 className="text-center text-2xl">You currently do not have any asset in portfolio.</h2>}
                <div className="bg-white rounded-lg">
                    {portfolio.length != 0 && portfolio.map(asset => {
                        return (
                            // onClick={() => setSymbol(asset.currency.symbol)}
                            // + (symbol === asset.currency.symbol ? "bg-slate-200/50" : "")
                            <div className={"grid grid-cols-3 flex items-center "} >
                                <div className="mx-5 p-5 flex items-center">
                                    <img src={asset.currency.image_url} alt="logo" width="40" className="rounded-xl"/>
                                    <div className="mx-5 font-bold">{asset.currency.name}</div>
                                </div>
                                <input type="text" className="rounded-lg p-2 bg-transparent outline-0" value={asset.amount} onChange={({target}) => handleChangeAmount(asset.id, target.value)}/>
                                <div className="flex justify-end">
                                    <button 
                                        className="mx-4 px-5 p-2 bg-red-500/50 rounded-xl font-bold hover:bg-red-500"
                                        onClick={() => handleDelete(asset.id)}
                                        >
                                            Delete
                                    </button>
                                </div>
                            </div>
                        )
                    })}
                </div>
            </div>
       </div>
    )
}