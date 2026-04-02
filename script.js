const messages = [
  "张威，今天你什么都不用证明，安心休息就好。",
  "你不是麻烦，你只是刚好在最需要被照顾的时候。",
  "今天状态不好也没关系，我在。",
  "你可以不坚强，但我会一直可靠。",
  "等你好一点，我带你去把想吃的都补回来。",
  "我最想做的事，就是让你少疼一点。"
];

const rotatingMessage = document.querySelector(".rotating-message");
const nextMessageButton = document.querySelector("[data-next-message]");
const openLetterButton = document.querySelector("[data-open-letter]");
const letterModal = document.querySelector("[data-letter-modal]");
const closeButtons = document.querySelectorAll("[data-close-letter]");
const checklistItems = document.querySelectorAll(".care-item");
const revealItems = document.querySelectorAll(".reveal");

let messageIndex = 0;

function renderMessage() {
  if (!rotatingMessage) return;
  rotatingMessage.textContent = messages[messageIndex];
}

function showNextMessage() {
  messageIndex = (messageIndex + 1) % messages.length;
  renderMessage();
}

function setModalState(open) {
  if (!letterModal) return;
  letterModal.hidden = !open;
  document.body.style.overflow = open ? "hidden" : "";
}

if (nextMessageButton) {
  nextMessageButton.addEventListener("click", showNextMessage);
}

if (openLetterButton) {
  openLetterButton.addEventListener("click", () => setModalState(true));
}

closeButtons.forEach((button) => {
  button.addEventListener("click", () => setModalState(false));
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setModalState(false);
  }
});

checklistItems.forEach((item) => {
  const checkbox = item.querySelector("input");
  if (!checkbox) return;

  checkbox.addEventListener("change", () => {
    item.classList.toggle("done", checkbox.checked);
  });
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in-view");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.18 }
);

revealItems.forEach((item) => observer.observe(item));

renderMessage();
