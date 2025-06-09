let params = new URLSearchParams(document.location.search);
let token = params.get("token");

function download_cert(name) {
    fetch('/api/download-cert', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        server_token: token,
        file_name: name
    })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = name; // filename for saving
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    });
}

let timeoutId;
const token_input = document.getElementById('token_text_input');

token_input.addEventListener('input', function() {
  if (timeoutId) {
    clearTimeout(timeoutId);
  }
  
  timeoutId = setTimeout(function() {
    const token = token_input.value;
    window.location.href = `/certs?token=${token}`;
  }, 500);
});



if (token) {
    token_input.value = token
}
