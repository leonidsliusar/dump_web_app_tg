async function start() {
WebApp.expand();
}

async function func() {
var firstNum = document.getElementById('first');
var secondNum = document.getElementById('second');
var result = document.getElementById('result');
result.innerHTML = parseFloat(firstNum.value) + parseFloat(secondNum.value)
}

async function closeApp() {
WebApp.close();
}

async function add_cart(data) {
var response = await fetch('/invoice', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
if (response.status === 200) {
var invoice = await response.json();
window.Telegram.WebApp.openInvoice(invoice);}
else {window.alert('error occurred')}
}

start()