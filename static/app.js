// Script para los mensajes flash (igual al de index.html)
document.addEventListener("DOMContentLoaded", function () {
  const messages = document.querySelectorAll(".message");
  messages.forEach((message) => {
    setTimeout(() => {
      message.classList.add("hidden");
      message.addEventListener("transitionend", () => {
        message.remove();
      });
    }, 5000);
  });
});
