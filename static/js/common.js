function wait(delay) {
    return new Promise((resolve) => setTimeout(resolve, delay));
}

window.httpGet = async function (url) {
    let resp = await fetch(url, {
        method: 'GET',
        cors: 'no-cors',
        redirect: 'follow'
    });
    return await resp.json();
}

window.httpPost = async function (url = '', data = {}) {
    let resp = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        redirect: 'follow',
        body: JSON.stringify(data),
    });
    console.log(resp);
    if (resp.status == 500) {
        wait(1000).then(() => {
            resp = fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow',
                body: JSON.stringify(data),
            });
        })
    }
    return await resp.json();
}