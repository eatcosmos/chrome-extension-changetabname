// 监听标签页更新
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // 检查是否是 DeepSeek 页面
  if (tab.url && tab.url.includes('chat.deepseek.com')) {
    // 发送消息到 content script
    chrome.tabs.sendMessage(tabId, {
      action: "checkTitle"
    }).catch(err => {
      // 忽略 "receiving end does not exist" 错误
      // 这个错误通常发生在页面还未完全加载时
      console.debug('Message failed:', err);
    });
  }
});

// 监听来自 content script 的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "titleUpdated") {
    console.debug('Title updated:', request.title);
  }
  // 必须返回 true 以支持异步响应
  return true;
}); 