document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const form = document.getElementById("ask-form");
  const userInput = document.getElementById("user-input");
  const typingIndicator = document.getElementById("typing-indicator");

  function appendMessage(sender, text, resources = {}) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);

    // Only text in chat
    const p = document.createElement("p");
    p.textContent = text;
    msgDiv.appendChild(p);

    // PPT
    if (resources.ppt && resources.ppt.length > 0) {
      const pptDiv = document.createElement("div");
      pptDiv.classList.add("resources");
      const title = document.createElement("strong");
      title.textContent = "PPT Resource:";
      pptDiv.appendChild(title);
      resources.ppt.forEach(r => {
        const a = document.createElement("a");
        a.href = r.url;
        a.textContent = r.title;
        a.target = "_blank";
        a.style.display = "block";
        pptDiv.appendChild(a);
      });
      msgDiv.appendChild(pptDiv);
    }

    // Video
    if (resources.video && resources.video.length > 0) {
      const videoDiv = document.createElement("div");
      videoDiv.classList.add("resources");
      const title = document.createElement("strong");
      title.textContent = "Video Resource:";
      videoDiv.appendChild(title);
      resources.video.forEach(r => {
        const a = document.createElement("a");
        a.href = r.url;
        a.textContent = r.title;
        a.target = "_blank";
        a.style.display = "block";
        videoDiv.appendChild(a);
      });
      msgDiv.appendChild(videoDiv);
    }

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = userInput.value.trim();
    if (!query) return;

    if (!query.toLowerCase().startsWith("explain ")) {
      appendMessage("jiji", "Please use the format: 'explain <topic>'");
      return;
    }

    const topic = query.slice(8).trim();
    if (!topic) {
      appendMessage("jiji", "Please provide a topic to explain.");
      return;
    }

    appendMessage("user", query);
    userInput.value = "";
    typingIndicator.classList.remove("hidden");

    try {
      const response = await fetch("/ask-jiji/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ question: topic })
      });

      const data = await response.json();
      typingIndicator.classList.add("hidden");

      appendMessage("jiji", data.answer, { ppt: data.ppt, video: data.video });

    } catch (err) {
      typingIndicator.classList.add("hidden");
      appendMessage("jiji", "Oops! Something went wrong.");
      console.error(err);
    }
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
