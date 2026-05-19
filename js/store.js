// ES6 Module - 全局状态管理
const store = {
    state: {},
    
    setState(key, value) {
        this.state[key] = value;
    },
    
    getState(key) {
        return key ? this.state[key] : this.state;
    }
};

// Window导出
window.store = store;

export { store };
