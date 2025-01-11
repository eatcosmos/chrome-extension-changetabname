// 存储定时器ID的对象
let intervalIds = {};

// 监听标签页更新
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (tab.url && tab.url.includes('chat.deepseek.com')) {
    // 清除可能存在的旧定时器
    if (intervalIds[tabId]) {
      clearInterval(intervalIds[tabId]);
    }
    
    // 设置新的定时器，每秒检查一次标题
    intervalIds[tabId] = setInterval(() => {
      chrome.tabs.sendMessage(tabId, { action: "checkTitle" });
    }, 1000);
  }
});

// 清理不再需要的定时器
chrome.tabs.onRemoved.addListener((tabId) => {
  if (intervalIds[tabId]) {
    clearInterval(intervalIds[tabId]);
    delete intervalIds[tabId];
  }
}); 