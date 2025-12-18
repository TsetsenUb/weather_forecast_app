import { getValidTokenPayload } from "./token.js";


function addLoginFormClickListeners () {
    const loginBtn = document.getElementById("loginBtn");
    const loginForm = document.getElementById("loginForm");
    const profileForm = document.getElementById("profileForm");
    const registerForm = document.getElementById("registerForm");
    const closeLogin = document.getElementById("closeLogin");

    loginBtn.addEventListener("click", function() {
        registerForm.classList.remove("active");
        loginForm.classList.toggle("active");
    });

    closeLogin.addEventListener("click", function() {
        loginForm.classList.remove("active");
    });
}

function addClickRemoveListener (event) {
    if (!event.target.closest(".nav-buttons")) {
        document.getElementById("loginForm").classList.remove("active");
        document.getElementById("registerForm").classList.remove("active");
        document.getElementById("profileForm").classList.remove("active");
    }
};

function hideLoginAndRegistration () {
    document.getElementById("loginForm").classList.remove("active");
    document.getElementById("loginBtn").classList.remove("active");
    document.getElementById("registerBtn").classList.remove("active");
}

function showLoginAndRegistration() {
    document.getElementById("loginBtn").classList.add("active");
    document.getElementById("registerBtn").classList.add("active");
}

function showProfileBtn (tokenPayload) {
    const profileBtn = document.getElementById("profileBtn");

    hideLoginAndRegistration();
    document.getElementById("cityInput").value = tokenPayload.address;

    profileBtn.textContent = tokenPayload.name;
    profileBtn.classList.add("active");
}

async function loginUser () {
    const errorMessage = document.getElementById("errorMessage");

    errorMessage.classList.remove("active");

    try {
        const formData = new FormData();
        formData.append("username", document.getElementById("loginEmail").value);
        formData.append("password", document.getElementById("loginPassword").value);

        const res = await fetch(`${window.location.origin}/api/users/token`, {
            method: "POST",
            body: formData,
        });

        if (res.status !== 201) {
            document.getElementById("cityInput").value = "";
            document.getElementById("weatherSection").classList.remove("active");
            const er = await res.json();
            throw new Error(er.detail || "Ошибка авторизации");
        }

        const tokenData = await res.json();
        localStorage.setItem("access_token", tokenData.access_token);
        localStorage.setItem("token_type", tokenData.token_type);

        showProfileBtn(getValidTokenPayload(tokenData.access_token));

    } catch (error) {
        console.error("Ошибка:", error);
        errorMessage.textContent = error.message || "Произошла ошибка при получении данных";
        errorMessage.classList.add("active");
    }
}

export {
    addLoginFormClickListeners,
    addClickRemoveListener,
    showLoginAndRegistration,
    loginUser,
};
