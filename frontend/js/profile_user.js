import { getValidTokenPayload } from "./token.js";


function addProfileFormClickListeners () {
    const profileBtn = document.getElementById("profileBtn");
    const profileForm = document.getElementById("profileForm");
    const closeProfile = document.getElementById("closeProfile");

    profileBtn.addEventListener("click", function() {
        profileForm.classList.toggle("active");
    });

    closeProfile.addEventListener("click", function() {
        profileForm.classList.remove("active");
    });
}

function addChangeBtnListener () {
    const changeBtn = document.getElementById("changeBtn");
    const closeChange = document.getElementById("closeChange");
    closeChange.classList.add("hidden");

    changeBtn.addEventListener("click", (event) => {
        event.preventDefault();
        document.getElementById("formButtons").classList.add("hidden");
        document.getElementById("closeProfile").classList.add("hidden");
        closeChange.classList.remove("hidden");

        document.querySelectorAll(".change-group").forEach(element => {
            element.classList.add("active");
        })

    })
}

function closeChangeForm () {
    const closeChange = document.getElementById("closeChange");

    document.getElementById("formButtons").classList.remove("hidden");
    document.getElementById("closeProfile").classList.remove("hidden");
    closeChange.classList.add("hidden");

    document.querySelectorAll(".change-group").forEach(element => {
        element.classList.remove("active");
    });
}

function addLogoutListener () {
    const logoutBtn = document.getElementById("logoutBtn");
    const profileBtn = document.getElementById("profileBtn");

    logoutBtn.addEventListener("click", (event) => {
        event.preventDefault();
        localStorage.removeItem("access_token");
        localStorage.removeItem("token_type");

        profileBtn.textContent = "";
        profileBtn.classList.remove("active");

        document.getElementById("loginEmail").value = "";
        document.getElementById("loginPassword").value = "";

        document.getElementById("profileForm").classList.remove("active");
        document.getElementById("loginBtn").classList.add("active");
        document.getElementById("registerBtn").classList.add("active");

    });
}

async function changeUserProfileData () {
    const newPassword = document.getElementById("changePassword").value;
    const newConfirmPassword = document.getElementById("changeConfirmPassword").value;

    if (newPassword && newPassword != newConfirmPassword) {
        alert("Пароли не совпадают!");
        return;
    }

    const newName = document.getElementById("changeName").value;
    const newEmail = document.getElementById("changeEmail").value;
    const newAddress = document.getElementById("changeCityName").value;

    let dataToUpdate = {};

    if (newName) { dataToUpdate.name = newName };
    if (newEmail) { dataToUpdate.email = newEmail };
    if (newPassword) { dataToUpdate.password = newPassword };
    if (newAddress) { dataToUpdate.address = newAddress };
    if (Object.keys(dataToUpdate).length == 0) {
        alert("Нет данных для обновления");
        return;
    };

    const cityInput = document.getElementById("cityInput");
    const weatherSection = document.getElementById("weatherSection");

    try {
        const res = await fetch(`${window.location.origin}/api/users/`, {
            method: "PATCH",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify(dataToUpdate),
        });

        const tokenData = await res.json();

        if (!res.ok) {
            throw new Error(tokenData.detail || "Ошибка обновления данных");
        }

        localStorage.setItem("access_token", tokenData.access_token);
        localStorage.setItem("token_type", tokenData.token_type);

        const tokenPayload = getValidTokenPayload(tokenData.access_token);

        alert("Данные успешно обновлены");
        cityInput.value = tokenPayload.address;
        document.getElementById("profileBtn").textContent = tokenPayload.name;
        weatherSection.classList.remove("active");

        closeChangeForm();

    } catch(error) {
        console.error("Ошибка:", error);
        const errorMessage = document.getElementById("errorMessage");
        errorMessage.textContent = error.message || "Произошла ошибка при получении данных";
        errorMessage.classList.add("active");
        cityInput.value = "";
        weatherSection.classList.remove("active");
    }
    document.getElementById("profileForm").classList.remove("active");
}

export {
    addProfileFormClickListeners,
    addChangeBtnListener,
    closeChangeForm,
    addLogoutListener,
    changeUserProfileData,
};
