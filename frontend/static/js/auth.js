function saveTokens(tokens) {
    localStorage.setItem('access_token', tokens.access_token);
    localStorage.setItem('refresh_token', tokens.refresh_token);
    localStorage.setItem('username', tokens.username);
}

function getAccessToken() {
    return localStorage.getItem('access_token');
}

function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
}

async function refreshToken() {
    try {
        const response = await fetch('/api/refresh', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getRefreshToken()}`
            }
        });
        const data = await response.json();
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token);
            return data.access_token;
        }
    } catch (error) {
        console.error('Error refreshing token:', error);
        clearTokens();
        window.location.href = '/login';
    }
} 