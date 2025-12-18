function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
            atob(base64)
                .split('')
                .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                .join('')
        );
        return JSON.parse(jsonPayload);
    } catch (error) {
        return null;
    }
}

function getValidTokenPayload(token) {
    if (!token) return false;

    const payload = parseJwt(token);
    if (!payload || !payload.exp) return false;
    if (Date.now() > payload.exp * 1000) return false;

    return payload;
}

export { getValidTokenPayload };
