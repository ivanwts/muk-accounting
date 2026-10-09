document.getElementById("year").textContent = new Date().getFullYear();
if (CONFIG.address) document.getElementById("legal-address").textContent = CONFIG.address;
if (CONFIG.email) {
  const e = document.getElementById("legal-email");
  e.textContent = CONFIG.email;
  e.href = "mailto:" + CONFIG.email;
}
