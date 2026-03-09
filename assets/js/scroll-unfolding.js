/**
 * 卷轴徐展式模态框 - 全局通用
 * 适用于：价值罗盘、人物卡牌、PPT预览等
 */

// 显示卷轴模态框
function showScrollUnfoldingModal(data) {
    // 移除已存在的模态框
    const existingModal = document.getElementById('scrollModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // 创建模态框HTML
    const modalHtml = `
        <div class="scroll-unfolding-modal" id="scrollModal">
            <div class="scroll-ink-bg"></div>
            <div class="scroll-paper-frame scroll-breathing">
                <button class="scroll-close-btn" onclick="closeScrollModal()" aria-label="关闭">
                    <i class="bi bi-x-lg" style="color: #8B4513;"></i>
                </button>
                <div class="scroll-bottom-rod"></div>
                <div class="scroll-content-area">
                    ${data.content || ''}
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // 触发动画
    requestAnimationFrame(() => {
        document.getElementById('scrollModal').classList.add('active');
    });
    
    document.body.style.overflow = 'hidden';
}

// 关闭卷轴模态框
function closeScrollModal() {
    const modal = document.getElementById('scrollModal');
    if (modal) {
        modal.classList.add('closing');
        setTimeout(() => {
            modal.remove();
            document.body.style.overflow = '';
        }, 400);
    }
}

// 事件委托 - 点击背景关闭
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('scroll-unfolding-modal')) {
        closeScrollModal();
    }
});

// ESC键关闭 - 仅当scrollModal存在时才响应
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && document.getElementById('scrollModal')) {
        closeScrollModal();
    }
});