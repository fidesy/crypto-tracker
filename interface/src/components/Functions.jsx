

const createUser = async (email) => {
    try {
        const resp = await fetch(
            `http://localhost:8000/users/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({email: email, password: "secretpassword"})
        })
        const res = await resp.json()
        return res.id
    } catch(e) {
        console.log(e)
    }
}

export const getUserByEmail = async (email) => {
    try {
        const resp = await fetch(`http://localhost:8000/users?email=${email}`)
        const res = await resp.json()
        if (res.detail === undefined) {
            return res.id
        } else {
            const id = await createUser(email)
            return id
        }
    } catch(e) {
        console.log(e)
    }
}


const createPortfolio = async (userID, title) => {
    try {
        const resp = await fetch(
            `http://localhost:8000/users/${userID}/portfolios/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({title: title})
        })
        const res = await resp.json()
        return res.id
    } catch(e) {
        console.log(e)
    }
}


export const fetchPortfolios = async (userID, portfolioTitle) => {
    try {
        const resp = await fetch(`http://localhost:8000/users/${userID}/portfolios/`)
        const res = await resp.json()

        if (res.detail !== undefined) return

        if (res.length === 0) {
            const id = await createPortfolio(userID, portfolioTitle)
            return id
        }

        return res[0].id

    } catch(e) {
        console.log(e)
    }
}