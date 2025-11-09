function addRegisterFormClickListeners () {
    const registerBtn = document.getElementById("registerBtn");
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const closeRegister = document.getElementById("closeRegister");

    registerBtn.addEventListener("click", function() {
        loginForm.classList.remove("active");
        registerForm.classList.toggle("active");
    });

    closeRegister.addEventListener("click", function() {
        registerForm.classList.remove("active");
    });
}

async function registrationUser () {
    const registerForm = document.getElementById("registerForm");
    const address = document.getElementById("registerCityName").value;
    const cityInput = document.getElementById("cityInput");
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.classList.remove("active");


    const newUserData = {
        name: document.getElementById("registerName").value,
        email: document.getElementById("registerEmail").value,
        password: document.getElementById("registerPassword").value,
        address: address,
    }

    const registerConfirmPassword = document.getElementById("registerConfirmPassword").value;

    if (newUserData.password != registerConfirmPassword) {
        alert("Пароли не совпадают!");
        return;
    }

    try {
        const weatherSection = document.getElementById("weatherSection");
        const res = await fetch("http://localhost:8000/api/users/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newUserData),
        });

        if (res.status != "201") {
            const er = await res.json();
            cityInput.value = "";
            weatherSection.classList.remove("active");
            throw new Error(er.detail || "Ошибка регистрации");
        }
        alert("Регистрация прошла успешно");
        if (address) {
            cityInput.value = address;
            weatherSection.classList.remove("active");
        }

    } catch (error) {
        console.error("Ошибка:", error);
        errorMessage.textContent = error.message || "Произошла ошибка при получении данных";
        errorMessage.classList.add("active");
    }
    registerForm.classList.remove("active");
}
