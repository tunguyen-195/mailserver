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