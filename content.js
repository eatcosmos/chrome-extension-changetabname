// 用于存储上一次的标题
let lastTitle = '';

// 检查并更新标题
function checkAndUpdateTitle() {
  const titleElement = document.querySelector('div.d8ed659a');
  if (titleElement) {
    const newTitle = titleElement.textContent.trim();
    if (newTitle && newTitle !== lastTitle && document.title !== newTitle) {
      document.title = newTitle;
      lastTitle = newTitle;
      // 通知 background script 标题已更新
      chrome.runtime.sendMessage({
        action: "titleUpdated",
        title: newTitle
      });
    }
  }
}

// 接收来自 background 的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "checkTitle") {
    checkAndUpdateTitle();
  }
});

// 创建 MutationObserver 来监视 DOM 变化
const observer = new MutationObserver((mutations) => {
  checkAndUpdateTitle();
});

// 开始观察文档变化
observer.observe(document.body, {
  childList: true,
  subtree: true
});

// 初始检查
checkAndUpdateTitle(); 