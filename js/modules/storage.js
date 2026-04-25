// 存储模块

const STORAGE_KEY = 'cognitive_training_v33';

function loadData() {
    try {
        const data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : { users: [], currentUser: null };
    } catch(e) {
        return { users: [], currentUser: null };
    }
}

function saveData(data) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

function getCurrentUserData() {
    const data = loadData();
    return data.users.find(u => u.id === data.currentUser);
}
