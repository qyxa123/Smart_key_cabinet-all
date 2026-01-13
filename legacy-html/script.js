// 智能钥匙柜管理系统 JavaScript 功能

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 初始化应用
function initializeApp() {
    // 设置当前日期为默认值
    setDefaultDates();
    
    // 初始化表单验证
    initializeFormValidation();
    
    // 初始化状态更新
    updateSystemStatus();
    
    // 添加页面动画效果
    addPageAnimations();
    
    // 初始化键盘事件
    initializeKeyboardEvents();
    
    // 初始化用户类型选择
    initializeUserTypeSelection();
}

// 设置默认日期
function setDefaultDates() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    // 设置借钥匙页面的默认日期
    const borrowDate = document.getElementById('borrowDate');
    const returnDate = document.getElementById('returnDate');
    const borrowTime = document.getElementById('borrowTime');
    const returnTime = document.getElementById('returnTime');
    
    if (borrowDate) {
        borrowDate.value = formatDate(today);
    }
    if (returnDate) {
        returnDate.value = formatDate(tomorrow);
    }
    if (borrowTime) {
        borrowTime.value = formatTime(today);
    }
    if (returnTime) {
        returnTime.value = formatTime(tomorrow);
    }
    
    // 设置还钥匙页面的默认日期
    const actualReturnDate = document.getElementById('actualReturnDate');
    const actualReturnTime = document.getElementById('actualReturnTime');
    
    if (actualReturnDate) {
        actualReturnDate.value = formatDate(today);
    }
    if (actualReturnTime) {
        actualReturnTime.value = formatTime(today);
    }
}

// 格式化日期为 YYYY-MM-DD 格式
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 格式化时间为 HH:MM 格式
function formatTime(date) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
}

// 初始化表单验证
function initializeFormValidation() {
    const borrowForm = document.getElementById('borrowForm');
    const returnForm = document.getElementById('returnForm');
    
    if (borrowForm) {
        borrowForm.addEventListener('submit', handleBorrowSubmit);
    }
    
    if (returnForm) {
        returnForm.addEventListener('submit', handleReturnSubmit);
    }
    
    // 添加实时验证
    addRealTimeValidation();
}

// 处理借钥匙表单提交
function handleBorrowSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    // 验证表单数据
    if (validateBorrowForm(data)) {
        showCompletionAnimation('借钥匙');
        // 这里可以添加实际的提交逻辑
        console.log('借钥匙数据:', data);
    }
}

// 处理还钥匙表单提交
function handleReturnSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    // 验证表单数据
    if (validateReturnForm(data)) {
        showCompletionAnimation('还钥匙');
        // 这里可以添加实际的提交逻辑
        console.log('还钥匙数据:', data);
    }
}

// 验证借钥匙表单
function validateBorrowForm(data) {
    const requiredFields = ['name', 'studentId', 'roomNumber', 'purpose', 'borrowDate', 'borrowTime', 'returnDate', 'returnTime'];
    
    // 根据用户类型调整验证规则
    if (data.userType === 'teacher') {
        // 老师必须填写电话
        if (!data.phone || data.phone.trim() === '') {
            showErrorMessage('老师必须填写联系电话');
            return false;
        }
        // 验证手机号格式
        if (data.phone && !validatePhone(data.phone)) {
            showErrorMessage('请输入正确的手机号码');
            return false;
        }
    }
    
    // 验证学号格式
    if (data.userType === 'student') {
        if (!validateStudentId(data.studentId)) {
            showErrorMessage('学生学号必须是6位数字');
            return false;
        }
    }
    
    for (let field of requiredFields) {
        if (!data[field] || data[field].trim() === '') {
            showErrorMessage(`请填写${getFieldLabel(field)}`);
            return false;
        }
    }
    
    // 验证门牌号格式
    if (!validateRoomNumber(data.roomNumber)) {
        showErrorMessage('门牌号格式不正确，请输入如101、205等格式');
        return false;
    }
    
    // 验证日期逻辑
    const borrowDateTime = new Date(`${data.borrowDate} ${data.borrowTime}`);
    const returnDateTime = new Date(`${data.returnDate} ${data.returnTime}`);
    
    if (returnDateTime <= borrowDateTime) {
        showErrorMessage('归还时间必须晚于借用时间');
        return false;
    }
    
    return true;
}

// 验证还钥匙表单
function validateReturnForm(data) {
    const requiredFields = ['returnName', 'returnStudentId', 'returnKeyNumber', 'returnRoomNumber', 'actualReturnDate', 'actualReturnTime'];
    
    for (let field of requiredFields) {
        if (!data[field] || data[field].trim() === '') {
            showErrorMessage(`请填写${getFieldLabel(field)}`);
            return false;
        }
    }
    
    // 验证门牌号格式
    if (!validateRoomNumber(data.returnRoomNumber)) {
        showErrorMessage('门牌号格式不正确，请输入如101、205等格式');
        return false;
    }
    
    return true;
}

// 获取字段标签
function getFieldLabel(field) {
    const labels = {
        'name': '姓名',
        'studentId': '学号/工号',
        'phone': '联系电话',
        'roomNumber': '门牌号',
        'purpose': '借用目的',
        'borrowDate': '借用日期',
        'borrowTime': '借用时间',
        'returnDate': '归还日期',
        'returnTime': '归还时间',
        'returnName': '姓名',
        'returnStudentId': '学号/工号',
        'returnKeyNumber': '钥匙编号',
        'returnRoomNumber': '门牌号',
        'actualReturnDate': '归还日期',
        'actualReturnTime': '归还时间'
    };
    return labels[field] || field;
}

// 验证手机号
function validatePhone(phone) {
    const phoneRegex = /^1[3-9]\d{9}$/;
    return phoneRegex.test(phone);
}

// 验证学号（6位数字）
function validateStudentId(studentId) {
    const studentIdRegex = /^\d{6}$/;
    return studentIdRegex.test(studentId);
}

// 验证门牌号格式
function validateRoomNumber(roomNumber) {
    const roomNumberRegex = /^\d{3}$/;
    return roomNumberRegex.test(roomNumber);
}

// 初始化用户类型选择
function initializeUserTypeSelection() {
    const userTypeRadios = document.querySelectorAll('input[name="userType"]');
    const phoneGroup = document.getElementById('phoneGroup');
    const phoneInput = document.getElementById('phone');
    const idLabel = document.getElementById('idLabel');
    const idLabelEn = document.getElementById('idLabelEn');
    const studentIdInput = document.getElementById('studentId');
    
    if (userTypeRadios.length > 0) {
        userTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'teacher') {
                    // 老师模式
                    if (phoneGroup) {
                        const label = phoneGroup.querySelector('label');
                        const subtitle = phoneGroup.querySelector('.bilingual-subtitle');
                        label.textContent = '联系电话 *';
                        if (subtitle) subtitle.textContent = 'Phone Number *';
                        phoneInput.required = true;
                    }
                    if (idLabel) {
                        idLabel.textContent = '工号 *';
                    }
                    if (idLabelEn) {
                        idLabelEn.textContent = 'Employee ID *';
                    }
                    if (studentIdInput) {
                        studentIdInput.placeholder = '请输入工号';
                    }
                } else if (this.value === 'student') {
                    // 学生模式
                    if (phoneGroup) {
                        const label = phoneGroup.querySelector('label');
                        const subtitle = phoneGroup.querySelector('.bilingual-subtitle');
                        label.textContent = '联系电话';
                        if (subtitle) subtitle.textContent = 'Phone Number';
                        phoneInput.required = false;
                    }
                    if (idLabel) {
                        idLabel.textContent = '学号 *';
                    }
                    if (idLabelEn) {
                        idLabelEn.textContent = 'Student ID *';
                    }
                    if (studentIdInput) {
                        studentIdInput.placeholder = '请输入6位学号 (如: 232120)';
                    }
                }
            });
        });
    }
}

// 添加实时验证
function addRealTimeValidation() {
    const inputs = document.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            clearFieldError(this);
        });
    });
}

// 验证单个字段
function validateField(field) {
    const value = field.value.trim();
    const isRequired = field.hasAttribute('required');
    
    if (isRequired && !value) {
        showFieldError(field, `${getFieldLabel(field.id)}不能为空`);
        return false;
    }
    
    if (field.type === 'tel' && value && !validatePhone(value)) {
        showFieldError(field, '请输入正确的手机号码');
        return false;
    }
    
    clearFieldError(field);
    return true;
}

// 显示字段错误
function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#ff6b6b';
    errorDiv.style.fontSize = '0.8rem';
    errorDiv.style.marginTop = '5px';
    
    field.parentNode.appendChild(errorDiv);
    field.style.borderColor = '#ff6b6b';
}

// 清除字段错误
function clearFieldError(field) {
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
    field.style.borderColor = '';
}

// 显示成功消息
function showSuccessMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'success-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-icon">✓</div>
            <div class="message-text">${message}</div>
        </div>
    `;
    
    // 添加样式
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(45deg, #00ff00, #00cc00);
        color: #000;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 255, 0, 0.3);
        z-index: 1000;
        animation: slideInRight 0.5s ease-out;
    `;
    
    document.body.appendChild(messageDiv);
    
    // 3秒后自动移除
    setTimeout(() => {
        messageDiv.style.animation = 'slideOutRight 0.5s ease-out';
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 500);
    }, 3000);
}

// 显示错误消息
function showErrorMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'error-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-icon">✗</div>
            <div class="message-text">${message}</div>
        </div>
    `;
    
    // 添加样式
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(45deg, #ff6b6b, #ff4444);
        color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
        z-index: 1000;
        animation: slideInRight 0.5s ease-out;
    `;
    
    document.body.appendChild(messageDiv);
    
    // 3秒后自动移除
    setTimeout(() => {
        messageDiv.style.animation = 'slideOutRight 0.5s ease-out';
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 500);
    }, 3000);
}

// 更新系统状态
function updateSystemStatus() {
    const availableKeys = document.getElementById('available-keys');
    const borrowedKeys = document.getElementById('borrowed-keys');
    
    if (availableKeys && borrowedKeys) {
        // 模拟实时数据更新
        setInterval(() => {
            const available = Math.floor(Math.random() * 5) + 20; // 20-24
            const borrowed = Math.floor(Math.random() * 3) + 5;  // 5-7
            
            availableKeys.textContent = available;
            borrowedKeys.textContent = borrowed;
            
            // 添加更新动画
            availableKeys.style.transform = 'scale(1.1)';
            borrowedKeys.style.transform = 'scale(1.1)';
            
            setTimeout(() => {
                availableKeys.style.transform = 'scale(1)';
                borrowedKeys.style.transform = 'scale(1)';
            }, 200);
        }, 5000);
    }
}

// 添加页面动画
function addPageAnimations() {
    // 为所有元素添加淡入动画
    const elements = document.querySelectorAll('.form-section, .status-item, .action-btn');
    
    elements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.6s ease-out';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// 初始化键盘事件
function initializeKeyboardEvents() {
    document.addEventListener('keydown', function(event) {
        // ESC键重置表单
        if (event.key === 'Escape') {
            const activeForm = document.querySelector('form');
            if (activeForm) {
                resetForm();
            }
        }
        
        // Enter键提交表单
        if (event.key === 'Enter' && event.ctrlKey) {
            const activeForm = document.querySelector('form');
            if (activeForm) {
                activeForm.dispatchEvent(new Event('submit'));
            }
        }
    });
}

// 重置表单
function resetForm() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.reset();
        
        // 清除所有错误状态
        const errorMessages = form.querySelectorAll('.field-error');
        errorMessages.forEach(error => error.remove());
        
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.style.borderColor = '';
        });
    });
    
    // 重新设置默认日期
    setDefaultDates();
    
    showSuccessMessage('表单已重置');
}

// 添加CSS动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .message-content {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .message-icon {
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .field-error {
        animation: fadeIn 0.3s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-5px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// 显示完成动画
function showCompletionAnimation(action) {
    // 创建全屏遮罩
    const overlay = document.createElement('div');
    overlay.className = 'completion-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(26, 26, 46, 0.95));
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.5s ease-out;
    `;
    
    // 创建完成内容
    const completionContent = document.createElement('div');
    completionContent.className = 'completion-content';
    completionContent.innerHTML = `
        <div class="completion-animation">
            <div class="success-icon">
                <div class="checkmark">
                    <div class="checkmark-stem"></div>
                    <div class="checkmark-kick"></div>
                </div>
            </div>
            <div class="completion-text">
                <h2>已完成</h2>
                <p>感谢使用济外国际智能钥匙柜管理系统</p>
                <div class="action-text">${action}操作已成功提交</div>
            </div>
            <div class="fireworks-container">
                <div class="firework firework-1"></div>
                <div class="firework firework-2"></div>
                <div class="firework firework-3"></div>
                <div class="firework firework-4"></div>
                <div class="firework firework-5"></div>
            </div>
        </div>
    `;
    
    // 添加样式
    const style = document.createElement('style');
    style.textContent = `
        .completion-content {
            text-align: center;
            color: #ffffff;
            position: relative;
        }
        
        .success-icon {
            width: 120px;
            height: 120px;
            margin: 0 auto 30px;
            position: relative;
            animation: successBounce 1s ease-out;
        }
        
        .checkmark {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: linear-gradient(45deg, #00ffff, #0080ff, #8000ff);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            animation: checkmarkRotate 2s ease-in-out infinite;
        }
        
        .checkmark-stem {
            width: 8px;
            height: 40px;
            background: #000;
            position: absolute;
            transform: rotate(45deg);
            border-radius: 4px;
            animation: checkmarkDraw 0.8s ease-out 0.5s both;
        }
        
        .checkmark-kick {
            width: 8px;
            height: 20px;
            background: #000;
            position: absolute;
            transform: rotate(-45deg);
            border-radius: 4px;
            animation: checkmarkDraw 0.6s ease-out 0.8s both;
        }
        
        .completion-text h2 {
            font-size: 3rem;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #00ffff, #0080ff, #8000ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: textGlow 2s ease-in-out infinite alternate;
        }
        
        .completion-text p {
            font-size: 1.5rem;
            margin-bottom: 15px;
            color: #aaa;
        }
        
        .action-text {
            font-size: 1.2rem;
            color: #00ffff;
            font-weight: bold;
        }
        
        .fireworks-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
        }
        
        .firework {
            position: absolute;
            width: 4px;
            height: 4px;
            border-radius: 50%;
            animation: fireworkExplode 2s ease-out infinite;
        }
        
        .firework-1 {
            top: 20%;
            left: 20%;
            background: #00ffff;
            animation-delay: 0s;
        }
        
        .firework-2 {
            top: 30%;
            left: 70%;
            background: #0080ff;
            animation-delay: 0.5s;
        }
        
        .firework-3 {
            top: 60%;
            left: 30%;
            background: #8000ff;
            animation-delay: 1s;
        }
        
        .firework-4 {
            top: 70%;
            left: 80%;
            background: #00ffff;
            animation-delay: 1.5s;
        }
        
        .firework-5 {
            top: 40%;
            left: 50%;
            background: #0080ff;
            animation-delay: 2s;
        }
        
        @keyframes successBounce {
            0% { transform: scale(0); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
        
        @keyframes checkmarkRotate {
            0%, 100% { transform: rotate(0deg); }
            50% { transform: rotate(5deg); }
        }
        
        @keyframes checkmarkDraw {
            0% { opacity: 0; transform: scale(0); }
            100% { opacity: 1; transform: scale(1); }
        }
        
        @keyframes textGlow {
            0% { text-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
            100% { text-shadow: 0 0 30px rgba(0, 128, 255, 0.8); }
        }
        
        @keyframes fireworkExplode {
            0% { 
                transform: scale(0);
                opacity: 1;
                box-shadow: 0 0 0 0 currentColor;
            }
            50% { 
                transform: scale(1);
                opacity: 1;
                box-shadow: 0 0 20px 10px currentColor;
            }
            100% { 
                transform: scale(3);
                opacity: 0;
                box-shadow: 0 0 40px 20px transparent;
            }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    overlay.appendChild(completionContent);
    document.body.appendChild(overlay);
    
    // 3秒后自动关闭
    setTimeout(() => {
        overlay.style.animation = 'fadeOut 0.5s ease-out';
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
            if (style.parentNode) {
                style.parentNode.removeChild(style);
            }
        }, 500);
    }, 3000);
    
    // 添加关闭动画样式
    const closeStyle = document.createElement('style');
    closeStyle.textContent = `
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
    `;
    document.head.appendChild(closeStyle);
}


// 导出函数供HTML调用
window.resetForm = resetForm;
