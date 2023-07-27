function onLoadRender(aLoginElement, authorizeUrl) {
    aLoginElement.href = authorizeUrl;
    aLoginElement.hidden = false;
}

function postLoginRender(logoutElement, welcomeMessageElement, nameElement, email) {
    logoutElement.onclick = function () {
        sessionStorage.clear();
        window.location.href = '/';
    };
    welcomeMessageElement.hidden = false;
    nameElement.innerText = email;
}

/**
 * Creates a URL for API access
 * @param {string} basePath
 * @param {string} path
 * @returns {URL}
 */

function apiJsonPathHelper(basePath, path) {
    const apiUrl = new URL(path, basePath);
    apiUrl.searchParams.append('dream.out.format', 'json');
    return apiUrl;
}

function fetchOptionsAuth(options = { headers: {} }) {
    const jwtSession = JSON.parse(sessionStorage.getItem('jwt'));
    if (options && options.headers) {
        options.headers.Authorization = `${jwtSession.token_type} ${jwtSession.access_token}`;
    }
    return options;
}

async function main() {
    const configResponse = await fetch('/config.json');
    const configJson = await configResponse.json();
    const params = new URLSearchParams(window.location.search);
    if (params.has('code')) {
        const tokenResponse = await fetch(`/token.json?code=${params.get('code')}`);
        const tokenJson = await tokenResponse.json();
        const tokenJsonStr = JSON.stringify(tokenJson);
        if (tokenJsonStr.length > 10) {
            sessionStorage.setItem('jwt', tokenJsonStr);
            document.location.href = '/';
        } else {
            alert('empty jwt');
        }
    } else if (sessionStorage.getItem('jwt') != null) {
        const apiUrl = apiJsonPathHelper(configJson.api, 'users/current');

        // Current user info request
        const currentUser = await (await fetch(apiUrl.toString(), fetchOptionsAuth())).json();
        postLoginRender(
            document.getElementById('logout'),
            document.getElementById('welcomeMessage'),
            document.getElementById('name'),
            currentUser.email
        );
    } else {
        onLoadRender(document.getElementById('login'), configJson.authorizeUrl);
    }
}

main();
