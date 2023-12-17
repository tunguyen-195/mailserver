function redirectToIndexWithDelay(delayInSeconds) {
    setTimeout(function() {
        window.location.href = 'http://127.0.0.1:5000/';
    }, delayInSeconds * 1000); // Chuyển đổi giây thành mili giây
}

// secret_key = ''
// function getKey() {
//     fetch('/get-secret-key'

//     ).then(function (res) {
//         return res.json()
//     }).then(function (data) {
//         secret_key = data
//         // console.log(secret_key)
//     }).catch(function (err) {
//     })
// };

document.addEventListener("DOMContentLoaded", () => {
  const cancelBonuses = document.querySelector(".app-cancel-bonuses");
  const app = document.querySelector(".app");

  const toggleBtn = document.querySelectorAll(".new-mail__toggle");
  toggleBtn.forEach(element => {
    element.addEventListener("click", () => {
      document.querySelector(".new-mail").classList.toggle("active");
      document.querySelector(".new__button").classList.toggle("active");
    });
  });

  cancelBonuses.addEventListener("click", () => {
    const classes = ["weird-rotate", "bonus-zoom", "bonus-exit"];
    app.classList.remove(...classes);
    byeCancelButton();
  });

  function byeCancelButton() {
    cancelBonuses.classList.toggle("app-cancel-bonuses--active");
  }

});


const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

const tabs = $$(".menu__item");
const panes = $$(".message-list");

tabs.forEach((tab, index) => {
  const pane = panes[index];

  tab.onclick = function () {
    $(".menu__item.active").classList.remove("active");
    $(".message-list.active").classList.remove("active");
    this.classList.add("active");
    pane.classList.add("active");
  };
});


function renderEmail(data){
    let subject = document.getElementById('open_subject')
    let sender = document.getElementById('open_sender')
    let sender_name = document.getElementById('open_sender_name')
    let content = document.getElementById('open_content')
    let received_at = document.getElementById('open_received_at')
    subject.innerText = data.subject
    sender.innerText = 'to: ' + data.sender
    sender_name.innerText = data.sender_name
    content.innerText = data.content
    received_at.innerText = data.received_at
};

function addToMails(id, subject, sender, content, received_at) {
    $(".preview-respond").classList.add("active");
    // console.log(content)
    fetch('/api/open-mail',{
        method: 'POST',
        body: JSON.stringify({
            'id': id,
            'subject': subject,
            'sender': sender,
            'content': content,
            'received_at': received_at
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (res) {
        return res.json()
    }).then(function (data) {
        // console.info(data);
        renderEmail(data)
    }).catch(function (err) {
        // console.error(err)
    })
};




// Toast function
function toast({ title = "", message = "", type = "info", duration = 3000 }) {
    const main = document.getElementById("toast");
    if (main) {
      const toast = document.createElement("div");
  
      // Auto remove toast
      const autoRemoveId = setTimeout(function () {
        main.removeChild(toast);
      }, duration + 1000);
  
      // Remove toast when clicked
      toast.onclick = function (e) {
        if (e.target.closest(".toast__close")) {
          main.removeChild(toast);
          clearTimeout(autoRemoveId);
        }
      };
  
      const icons = {
        success: "fas fa-check-circle",
        info: "fas fa-info-circle",
        warning: "fas fa-exclamation-circle",
        error: "fas fa-exclamation-circle"
      };
      const icon = icons[type];
      const delay = (duration / 1000).toFixed(2);
  
      toast.classList.add("toast", `toast--${type}`);
      toast.style.animation = `slideInLeft ease .3s, fadeOut linear 1s ${delay}s forwards`;
  
      toast.innerHTML = `
                      <div class="toast__icon">
                          <i class="${icon}"></i>
                      </div>
                      <div class="toast__body">
                          <h3 class="toast__title">${title}</h3>
                          <p class="toast__msg">${message}</p>
                      </div>
                      <div class="toast__close">
                          <i class="fas fa-times"></i>
                      </div>
                  `;
      main.appendChild(toast);
    }
  }
  
  function showSuccessToast() {
    toast({
      title: "Thành công!",
      message: "Email của bạn đã được gửi!",
      type: "success",
      duration: 5000
    });
  }
  
  function showErrorToast() {
    toast({
      title: "Thất bại!",
      message: "Có lỗi xảy ra, vui lòng liên hệ quản trị viên.",
      type: "error",
      duration: 5000
    });
  }
  
  function switchToast(res){
    if(res){
      showSuccessToast();
    }
    else{
      showErrorToast();
    }
  }


  // Send mail
  function cleanInput(){
    document.getElementById('emailInput').value = ''
    document.getElementById('objectInput').value = ''
    document.getElementById('messageTextarea').value = ''
}
function Mailing(){
    const email = document.getElementById('emailInput').value
    const title = document.getElementById('objectInput').value
    const message = document.getElementById('messageTextarea').value
    cleanInput()
    console.log(email, title, message)
    fetch('/api/send-mail',{
        method: 'POST',
        body: JSON.stringify({
        'email': email,
        'title': title,
        'message': message
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (res) {
        if (res.ok) {
            return res
        } else {
            throw new Error('Request failed');
        }
    }).then(function (data) {
        switchToast(true)
        redirectToIndexWithDelay(3);
    }).catch(function (err) {
        switchToast(false)
    })
}