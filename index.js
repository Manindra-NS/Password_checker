const pwdInput = document.getElementById('password');
const toggleBtn = document.getElementById('toggleBtn');
const eyeIcon = document.getElementById('eye');

toggleBtn.addEventListener('click', () => {
  const isHidden = pwdInput.type === 'password';
  pwdInput.type = isHidden ? 'text' : 'password';
  eyeIcon.classList.toggle('fa-eye');
  eyeIcon.classList.toggle('fa-eye-slash');
  toggleBtn.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
});



const passwordInput = document.getElementById("password");
const checkButton = document.querySelector(".check");

checkButton.addEventListener("click", async () => {
  const password = passwordInput.value;

  if (!password) {
    return; // nothing to check
  }

  let data;
  try {
    const response = await fetch("/api/check-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    data = await response.json();
  } catch (err) {
    console.error("Could not reach the password-check server:", err);
    return;
  }

  updateChecklist(data.checks);
  updateScore(data.score, data.entropy);
  updateStatus("common-result", data.common);
  updateStatus("breached-result", data.breached);
});

// Toggles a checklist <li> between cross/tick based on a boolean
function updateChecklist(checks) {
  setCheckItem("check-uppercase", checks.uppercase);
  setCheckItem("check-lowercase", checks.lowercase);
  setCheckItem("check-digit", checks.digit);
  setCheckItem("check-special", checks.special);
}

function setCheckItem(id, passed) {
  const item = document.getElementById(id);
  const icon = item.querySelector("i");

  item.classList.toggle("passed", passed);
  icon.classList.toggle("fa-check", passed);
  icon.classList.toggle("icon-tick", passed);
  icon.classList.toggle("fa-xmark", !passed);
  icon.classList.toggle("icon-cross", !passed);
}

// Fills in the score number/label and entropy value
function updateScore(score, entropy) {
  const scoreValue = document.getElementById("score-value");
  const scoreLabel = document.getElementById("score-label");
  const entropyValue = document.getElementById("entropy-value");

  scoreValue.textContent = score.points;
  scoreLabel.textContent = capitalize(score.label);
  entropyValue.textContent = entropy.toFixed(1);

  scoreLabel.classList.remove(
    "label-weak",
    "label-moderate",
    "label-strong",
    "label-strongest"
  );
  scoreLabel.classList.add(`label-${score.label}`);
}

// Handles the common-password / breached rows.
// value can be true, false, or null (breach check could not be performed)
function updateStatus(id, value) {
  const row = document.getElementById(id);
  const icon = row.querySelector("i");
  const label = row.querySelector("span");

  row.classList.remove("status-yes", "status-no");

  if (value === null) {
    label.textContent = "Unknown";
    icon.classList.remove("fa-check", "icon-tick");
    icon.classList.add("fa-xmark", "icon-cross");
    return;
  }

  row.classList.add(value ? "status-yes" : "status-no");
  label.textContent = value ? "Yes" : "No";
  icon.classList.toggle("fa-check", value);
  icon.classList.toggle("icon-tick", value);
  icon.classList.toggle("fa-xmark", !value);
  icon.classList.toggle("icon-cross", !value);
}

function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}