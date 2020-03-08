
const globalStore = [];

class Store {
  constructor(data) {
    globalStore.push(this);
    this.callbacks = {};
    this.initialized = false;
    Object.keys(data).forEach((key) => {
      this[key] = data[key];
    });
  }

  setState(data) {
    this.initialized = true;
    // console.log(data);
    Object.keys(data).forEach((key) => {
      this[key] = data[key];
    });
    return this;
  }

  setCallback(name, callback) {
    this.callbacks[name] = callback;
  }

  delCallback(name) {
    delete this.callbacks[name];
  }

  refresh(name) {
    const isName = !!name;
    if (isName) {
      // console.log(`state.Store refresh ${name}`);
      if (this.callbacks[name]) this.callbacks[name]();
    } else {
      Object.keys(this.callbacks).forEach((key) => {
        console.log(`state.Store refresh ${key}`);
        this.callbacks[key]();
      });
    }
  }
}

window.globalStore = globalStore;

export default Store;
