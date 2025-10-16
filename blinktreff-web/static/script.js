async function sendSkudd() {
  const skytter = document.getElementById("skytter").value;
  const skive = document.getElementById("skive").value;
  const x = parseFloat(document.getElementById("x").value);
  const y = parseFloat(document.getElementById("y").value);

  const res = await fetch("/registrer_skudd", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ skytter, skive, x, y })
  });
  const data = await res.json();
  document.getElementById("resultat").innerText = `Poeng: ${data.poeng}`;
}