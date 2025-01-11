// 接收来自 background 的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "checkTitle") {
    const titleElement = document.querySelector('div.d8ed659a');
    if (titleElement && document.title !== titleElement.textContent.trim()) {
      document.title = titleElement.textContent.trim();
    }
  }
}); 