import { getValidTokenPayload } from "./token.js";

import {
    addLoginFormClickListeners,
    addClickRemoveListener,
    showLoginAndRegistration,
    showProfileBtn,
    loginUser,
} from "./login_user.js";

import {
    addProfileFormClickListeners,
    addChangeBtnListener,
    closeChangeForm,
    addLogoutListener,
    changeUserProfileData,
} from "./profile_user.js";

import {
    addRegisterFormClickListeners,
    registrationUser
} from "./registration_user.js";

import { getAndDisplayForecast } from "./weather.js";


document.addEventListener("DOMContentLoaded", async function() {
    const tokenPayload = getValidTokenPayload(localStorage.getItem("access_token"));

    if (tokenPayload) {
        showProfileBtn(tokenPayload);
        await getAndDisplayForecast();
    } else {
        showLoginAndRegistration();
    }

    addLoginFormClickListeners();
    addRegisterFormClickListeners();
    addProfileFormClickListeners();
    addChangeBtnListener();
    closeChangeForm();
    addLogoutListener();

    document.getElementById("loginForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        await loginUser();
        if (document.getElementById("cityInput").value) {
            await getAndDisplayForecast();
        }
    });

    document.getElementById("registerForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        await registrationUser();
    })

    document.getElementById("weatherForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        await getAndDisplayForecast();
    });

    document.getElementById("closeChange").addEventListener("click", (event) => {
        event.preventDefault();
        closeChangeForm();
    });

    document.getElementById("profileForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        await changeUserProfileData();
    });

    document.addEventListener("click", function(event) {
        addClickRemoveListener(event);
    });
});
