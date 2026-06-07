document.getElementById('cv').addEventListener('change', function () {
  const label = document.getElementById('fileLabel');
  const area = document.getElementById('fileArea');
  if (this.files[0]) {
    label.textContent = this.files[0].name;
    label.className = 'filename';
    area.classList.add('has-file');
  }
});

async function submitForm() {
  const name = document.getElementById('name').value.trim();
  const last_name = document.getElementById('last_name').value.trim();
  const email = document.getElementById('email').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const cv = document.getElementById('cv').files[0];
  const btn = document.getElementById('submitBtn');
  const btnText = document.getElementById('btnText');
  const btnSpinner = document.getElementById('btnSpinner');

  if (!name || !last_name || !email || !phone || !cv) {
    showMessage('Please fill in all fields and attach your CV.', 'error');
    return;
  }

  const formData = new FormData();
  formData.append('name', name);
  formData.append('last_name', last_name);
  formData.append('email', email);
  formData.append('phone', phone);
  formData.append('cv', cv);

  btn.disabled = true;
  btnText.textContent = 'Sending...';
  btnSpinner.classList.remove('hidden');

  try {
    const response = await fetch('http://127.0.0.1:8001/api/upload', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (response.ok) {
      showMessage(`✅ Application sent successfully!`, 'success');
      btnText.textContent = 'Sent!';
      btnSpinner.classList.add('hidden');
    } else {
      showMessage(`❌ Error: ${data.detail}`, 'error');
      resetBtn();
    }
  } catch (err) {
    showMessage('❌ Could not connect to the server. Try again later.', 'error');
    resetBtn();
  }
}

function resetBtn() {
  const btn = document.getElementById('submitBtn');
  const btnText = document.getElementById('btnText');
  const btnSpinner = document.getElementById('btnSpinner');
  btn.disabled = false;
  btnText.textContent = 'Send application';
  btnSpinner.classList.add('hidden');
}

function showMessage(text, type) {
  const msg = document.getElementById('message');
  msg.textContent = text;
  msg.className = `message ${type}`;
  msg.classList.remove('hidden');
}
