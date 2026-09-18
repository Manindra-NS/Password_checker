const passwordInput = document.getElementById("password");
const togglePasswordButton = document.getElementById("toggleBtn");
const checkButton = document.querySelector(".check");

togglePasswordButton.addEventListener("click", () => {
  const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
  passwordInput.setAttribute("type", type);
  togglePasswordButton.innerHTML = type === "password" ? "<i class='fa-regular fa-eye'></i>" : "<i class='fa-regular fa-eye-slash'></i>";
});

checkButton.addEventListener("click",async ()=>{
  const password = passwordInput.value;
  console.log(password);

  const response = await fetch("http://localhost:5000/check-password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({password})
  });

  const result = await response.json();
  console.log("result:", result);
  document.getElementById("score-value").textContent = result.analysis.points;
  document.getElementById("score-label").textContent = result.analysis.label;
  const scoreLabel = document.getElementById("score-label");
  scoreLabel.className = "score-label label-" + result.analysis.label;
  document.getElementById("entropy-value").textContent = result.entropy.toFixed(2);

  
  document.getElementById("check-uppercase").innerHTML = result.analysis.hasUpper
    ? "<i class='fa-solid fa-check' style='color: rgb(99, 230, 190);'></i> Have an uppercase letter"
    : "<i class='fa-solid fa-xmark icon-cross'></i> Don't have an uppercase letter";
  document.getElementById("check-lowercase").innerHTML = result.analysis.hasLower
    ? "<i class='fa-solid fa-check' style='color: rgb(99, 230, 190);'></i> Have a lowercase letter"
    : "<i class='fa-solid fa-xmark icon-cross'></i> Don't have a lowercase letter";
  document.getElementById("check-digit").innerHTML = result.analysis.hasDigit
    ? "<i class='fa-solid fa-check' style='color: rgb(99, 230, 190);'></i> Have a digit"
    : "<i class='fa-solid fa-xmark icon-cross'></i> Don't have a digit";
  document.getElementById("check-special").innerHTML = result.analysis.hasSpecial
    ? "<i class='fa-solid fa-check' style='color: rgb(99, 230, 190);'></i> Have a special character"
    : "<i class='fa-solid fa-xmark icon-cross'></i> Don't have a special character";
    
    
  document.getElementById("common-result").innerHTML = result.commonPassword 
    ? "<i class='fa-solid fa-check'style='color: rgb(99, 230, 190);'></i> Yes" 
    : "<i class='fa-solid fa-xmark icon-cross'></i> No";
  document.getElementById("breached-result").innerHTML = result.breached 
    ? "<i class='fa-solid fa-check'style='color: rgb(99, 230, 190);'></i> Yes" 
    : "<i class='fa-solid fa-xmark icon-cross'></i> No";
});

